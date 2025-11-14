"""
XBot v2.1 - Reconstructed Source Code
Based on bytecode analysis, string extraction, and behavioral patterns

This shows what the actual implementation likely looks like.
Reconstructed for defensive analysis and understanding attack techniques.
"""

import asyncio
import math
import re
import uuid
import json
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import keyring
import flet as ft
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

VERSION = "XBot V2.1"
ALTERNATE_NAME = "DolphinBot"

# Files
PROFILES_FILE = ".xbot_profiles.json"
SETTINGS_FILE = ".settings.json"

# Keyring service identifiers
SERVICE_CLIENT_ID = "XBot"
SERVICE_PASSWORD = "XBot.py"

# Default settings
DEFAULT_SETTINGS = {
    "drop_limit": 50,
    "drop_sleep": 5,
    "after_drops": None,
    "rate_limit_sleep": 60,
    "group_skip": [],
    "leniency_1_3": True,
    "leniency_1_4": True,
    "leniency_2_5": True,
    "gif_keyword": "hello",
    "randomize": True,
    "no_gif": False,
    "drop_message": "Hit my pinned post\nPlease add me to your groups",
    "skip_chudai": True,
    "skip_missing_followers": True,
    "skip_non_of_link": True,
    "assume_invalid_room_as_three": False,
}


# =============================================================================
# TWITTER AUTOMATION ENGINE
# =============================================================================

class TwitterAutomation:
    """
    Core Twitter automation using Playwright browser automation
    """

    def __init__(self, profile, settings):
        self.profile = profile
        self.settings = settings
        self.browser = None
        self.page = None
        self.drop_count = 0
        self.is_rate_limited = False

    async def start(self):
        """Initialize browser and login to Twitter"""
        playwright = await async_playwright().start()

        # Launch browser (headless or visible based on settings)
        self.browser = await playwright.chromium.launch(
            headless=False,  # Usually visible for debugging
            args=['--disable-blink-features=AutomationControlled']
        )

        # Create new page
        context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await context.new_page()

        # Login to Twitter
        await self._login_twitter()

    async def _login_twitter(self):
        """
        Login to Twitter using stored credentials
        """
        try:
            # Navigate to Twitter login
            await self.page.goto('https://twitter.com/i/flow/login', timeout=30000)
            await asyncio.sleep(2)

            # Enter username/email
            username_input = await self.page.wait_for_selector('input[autocomplete="username"]')
            await username_input.fill(self.profile['email'])
            await asyncio.sleep(0.5)

            # Click next
            next_button = await self.page.wait_for_selector('button:has-text("Next")')
            await next_button.click()
            await asyncio.sleep(2)

            # Enter password
            password = keyring.get_password(SERVICE_CLIENT_ID, self.profile['client_id'])
            password_input = await self.page.wait_for_selector('input[type="password"]')
            await password_input.fill(password)
            await asyncio.sleep(0.5)

            # Click login
            login_button = await self.page.wait_for_selector('button[data-testid="LoginForm_Login_Button"]')
            await login_button.click()

            # Wait for home page
            await self.page.wait_for_url('https://twitter.com/home', timeout=15000)
            await asyncio.sleep(3)

            print(f"[+] Logged in as {self.profile['username']}")

        except Exception as e:
            print(f"[-] Login failed: {e}")
            raise

    async def run_drops(self, targets):
        """
        Main automation loop - post messages to targets

        Args:
            targets: List of Twitter users/groups to message
        """
        for target in targets:
            # Check if should skip
            if self._should_skip_target(target):
                print(f"[*] Skipping target: {target['name']}")
                continue

            # Check if reached limit
            if self.drop_count >= self.settings['drop_limit']:
                print(f"[+] Reached drop limit ({self.settings['drop_limit']})")
                break

            # Post message to target
            try:
                await self._post_to_target(target)
                self.drop_count += 1
                print(f"[+] Drop {self.drop_count}/{self.settings['drop_limit']} completed")

                # Sleep between drops
                sleep_time = self.settings['drop_sleep']
                if self.settings['randomize']:
                    # Add random variance (-20% to +20%)
                    variance = sleep_time * 0.2
                    sleep_time += (math.random() - 0.5) * 2 * variance

                print(f"[*] Sleeping for {sleep_time:.1f} seconds...")
                await asyncio.sleep(sleep_time)

            except RateLimitError:
                print(f"[!] Rate limited! Sleeping for {self.settings['rate_limit_sleep']} seconds...")
                await asyncio.sleep(self.settings['rate_limit_sleep'])
                self.is_rate_limited = True

            except Exception as e:
                print(f"[-] Error posting to {target['name']}: {e}")
                continue

    def _should_skip_target(self, target):
        """
        Determine if target should be skipped based on settings
        """
        # Skip if in skip list
        if target['id'] in self.settings['group_skip']:
            return True

        # Skip if no followers (evasion tactic)
        if self.settings['skip_missing_followers'] and target.get('followers', 0) == 0:
            return True

        # Skip based on other criteria
        if self.settings['skip_chudai'] and 'chudai' in target.get('name', '').lower():
            return True

        if self.settings['skip_non_of_link'] and not target.get('has_onlyfans_link'):
            return True

        return False

    async def _post_to_target(self, target):
        """
        Post spam message to a specific target

        Process:
        1. Navigate to target's DM or group
        2. Type the spam message
        3. Optionally attach GIF
        4. Click send
        """
        try:
            # Navigate to messages
            await self.page.goto(f'https://twitter.com/messages/compose', timeout=15000)
            await asyncio.sleep(2)

            # Search for target
            search_input = await self.page.wait_for_selector('[data-testid="dmComposerSearchInput"]')
            await search_input.fill(target['username'])
            await asyncio.sleep(1)

            # Select first result
            first_result = await self.page.wait_for_selector('[data-testid="TypeaheadUser"]')
            await first_result.click()
            await asyncio.sleep(1)

            # Type message
            message_box = await self.page.wait_for_selector('[data-testid="dmComposerTextInput"]')

            # Type message with human-like delays
            message = self.settings['drop_message']
            for char in message:
                await message_box.type(char, delay=50 + math.random() * 50)

            await asyncio.sleep(0.5)

            # Attach GIF if enabled
            if not self.settings['no_gif']:
                await self._attach_gif()

            # Click send button
            send_button = await self.page.wait_for_selector('[data-testid="dmComposerSendButton"]')
            await send_button.click()

            await asyncio.sleep(1)

            # Check for rate limit indicators
            if await self._check_rate_limit():
                raise RateLimitError("Rate limit detected")

        except PlaywrightTimeout:
            print(f"[-] Timeout posting to {target['username']}")
            raise

    async def _attach_gif(self):
        """
        Attach a GIF to the message

        Uses Twitter's GIF search with configured keyword
        """
        try:
            # Click GIF button
            gif_button = await self.page.wait_for_selector('[data-testid="dmComposerGifButton"]')
            await gif_button.click()
            await asyncio.sleep(1)

            # Search for GIF
            gif_search = await self.page.wait_for_selector('[placeholder="Search GIFs"]')
            await gif_search.fill(self.settings['gif_keyword'])
            await asyncio.sleep(1.5)

            # Select random GIF or first one
            if self.settings['randomize']:
                # Get all GIF results
                gifs = await self.page.query_selector_all('[data-testid="gif-result"]')
                if gifs:
                    import random
                    selected_gif = random.choice(gifs[:9])  # Choose from first 9
                    await selected_gif.click()
            else:
                # Click first GIF
                first_gif = await self.page.wait_for_selector('[data-testid="gif-result"]')
                await first_gif.click()

            await asyncio.sleep(0.5)

        except Exception as e:
            print(f"[-] Failed to attach GIF: {e}")
            # Continue without GIF

    async def _check_rate_limit(self):
        """
        Check if Twitter has rate limited the account

        Looks for error messages or rate limit indicators
        """
        # Check for rate limit error text
        error_texts = [
            "You are over the daily limit",
            "Try again later",
            "Rate limit exceeded",
        ]

        for error_text in error_texts:
            if await self.page.locator(f'text="{error_text}"').count() > 0:
                return True

        return False

    async def close(self):
        """Cleanup and close browser"""
        if self.browser:
            await self.browser.close()
            print("[*] Browser closed")


class RateLimitError(Exception):
    """Raised when Twitter rate limiting is detected"""
    pass


# =============================================================================
# PROFILE & SETTINGS MANAGEMENT
# =============================================================================

class ProfileManager:
    """Manages Twitter account profiles and settings"""

    def __init__(self):
        self.profiles = []
        self.settings = DEFAULT_SETTINGS.copy()
        self.saved_profiles = {}

    def load_profiles(self):
        """Load profiles from .xbot_profiles.json"""
        profiles_file = Path(PROFILES_FILE)
        if profiles_file.exists():
            with open(profiles_file, 'r') as f:
                data = json.load(f)
                self.profiles = data.get('profiles', [])
            print(f"[+] Loaded {len(self.profiles)} profiles")

    def save_profiles(self):
        """Save profiles to .xbot_profiles.json"""
        with open(PROFILES_FILE, 'w') as f:
            json.dump({'profiles': self.profiles}, f, indent=2)
        print(f"[+] Saved {len(self.profiles)} profiles")

    def add_profile(self, username, email, password, license_key=None):
        """
        Add new Twitter account profile

        Args:
            username: Twitter handle
            email: Account email
            password: Account password (stored in keyring)
            license_key: XBot license key
        """
        profile_id = str(uuid.uuid4())
        client_id = f"client_{profile_id}"

        # Store password in keyring
        keyring.set_password(SERVICE_CLIENT_ID, client_id, password)

        # Add to profiles
        profile = {
            'id': profile_id,
            'username': username,
            'email': email,
            'client_id': client_id,
            'tag': username,
            'license_key': license_key
        }

        self.profiles.append(profile)
        self.save_profiles()

        print(f"[+] Added profile: {username}")

    def get_profile_password(self, profile):
        """Retrieve password from keyring"""
        return keyring.get_password(SERVICE_CLIENT_ID, profile['client_id'])

    def load_settings(self):
        """Load settings from .settings.json"""
        settings_file = Path(SETTINGS_FILE)
        if settings_file.exists():
            with open(settings_file, 'r') as f:
                data = json.load(f)
                self.settings = data.get('all_settings', DEFAULT_SETTINGS)
                self.saved_profiles = data.get('saved_profiles', {})
            print("[+] Loaded settings")

    def save_settings(self):
        """Save settings to .settings.json"""
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({
                'all_settings': self.settings,
                'saved_profiles': self.saved_profiles
            }, f, indent=2)
        print("[+] Saved settings")


# =============================================================================
# GUI APPLICATION (Flet)
# =============================================================================

class XBotApp:
    """Main GUI application"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.profile_manager = ProfileManager()
        self.running_tasks = {}  # profile_id -> automation task

        # Load data
        self.profile_manager.load_profiles()
        self.profile_manager.load_settings()

    def run_bootstrap(self):
        """Show identity creation screen"""
        self.page.title = "XBot V2.1"
        self.page.window_width = 800
        self.page.window_height = 600

        # Simple identity screen
        def on_submit(e):
            # Create identity and go to main screen
            self.run_main()

        self.page.add(
            ft.Column([
                ft.Text("Welcome to XBOT", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Please purchase from @PurchaseTwitterXBot on Telegram instead.",
                       color=ft.colors.RED),
                ft.ElevatedButton("Continue", on_click=on_submit)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def run_main(self):
        """Show main dashboard"""
        self.page.clean()

        # Build profile list
        profile_list = ft.ListView(spacing=10)

        for profile in self.profile_manager.profiles:
            profile_row = self._build_profile_row(profile)
            profile_list.controls.append(profile_row)

        # Main layout
        self.page.add(
            ft.Column([
                ft.Text("XBOT Dashboard", size=24, weight=ft.FontWeight.BOLD),
                profile_list,
                ft.Row([
                    ft.ElevatedButton("Add Profile", on_click=self._show_add_profile_dialog),
                    ft.ElevatedButton("Settings", on_click=self._show_settings_dialog)
                ])
            ])
        )

    def _build_profile_row(self, profile):
        """Build UI row for a profile"""
        async def on_run(e):
            if profile['id'] in self.running_tasks:
                # Stop
                task = self.running_tasks[profile['id']]
                task.cancel()
                del self.running_tasks[profile['id']]
                run_button.text = "Run"
            else:
                # Start
                run_button.text = "Stop"
                task = asyncio.create_task(self._run_profile(profile))
                self.running_tasks[profile['id']] = task

            self.page.update()

        run_button = ft.ElevatedButton("Run", on_click=on_run)

        return ft.Row([
            ft.Text(profile['username']),
            ft.Text(profile.get('tag', '')),
            run_button,
            ft.IconButton(icon=ft.icons.SETTINGS, on_click=lambda e: self._show_settings_dialog(e))
        ])

    async def _run_profile(self, profile):
        """Run automation for a profile"""
        print(f"[*] Starting automation for {profile['username']}")

        # Get targets (hardcoded example - real version would load from somewhere)
        targets = [
            {'id': '1', 'username': 'user1', 'name': 'User 1', 'followers': 100},
            {'id': '2', 'username': 'user2', 'name': 'User 2', 'followers': 50},
            # ... more targets
        ]

        # Create automation instance
        automation = TwitterAutomation(profile, self.profile_manager.settings)

        try:
            await automation.start()
            await automation.run_drops(targets)
        except Exception as e:
            print(f"[-] Automation error: {e}")
        finally:
            await automation.close()

    def _show_add_profile_dialog(self, e):
        """Show dialog to add new profile"""
        # Dialog implementation
        pass

    def _show_settings_dialog(self, e):
        """Show settings dialog"""
        # Settings dialog with sliders, text inputs, etc.
        pass


# =============================================================================
# LICENSE SYSTEM (Cracked)
# =============================================================================

class LicenseManager:
    """
    Handles license validation

    Original: Contacts license server API
    Cracked: Always returns valid
    """

    API_BASE = None  # Original API endpoint (removed/bypassed)

    @staticmethod
    def check_license(license_key):
        """
        Validate license key

        In cracked version, always returns True
        """
        print("Please purchase from @PurchaseTwitterXBot on Telegram instead.")
        return {
            'valid': True,
            'tier': 'premium',
            'expires': None,  # Bypassed
            'features': ['unlimited_drops', 'multiple_accounts', 'scheduling']
        }


# =============================================================================
# ENTRY POINTS
# =============================================================================

def bootstrap(page: ft.Page):
    """Entry point: show identity screen"""
    app = XBotApp(page)
    app.run_bootstrap()


def main(page: ft.Page):
    """Entry point: show main dashboard"""
    app = XBotApp(page)
    app.run_main()


if __name__ == "__main__":
    # Run GUI application
    ft.app(target=bootstrap)
