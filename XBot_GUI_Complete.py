"""
XBot GUI Implementation - Complete Flet-based Interface
Reconstructed from string analysis and UI patterns
"""

import flet as ft
import asyncio
from datetime import datetime
import random


class XBotGUI:
    """
    Complete GUI implementation using Flet framework

    Screens:
    1. Bootstrap - Identity creation/restoration
    2. Main Dashboard - Profile management and controls
    3. Settings Dialog - Bot configuration
    4. Purchase Dialog - License/payment (bypassed)
    5. License Management - Key entry and status
    """

    def __init__(self, page: ft.Page, app):
        self.page = page
        self.app = app

        # UI state
        self.profile_rows = {}
        self.status_indicators = {}
        self.progress_bars = {}

        # Animation particles
        self.particles = []
        self.particle_task = None

    # =========================================================================
    # PAGE CONFIGURATION
    # =========================================================================

    def configure_page(self):
        """Configure main window appearance"""
        self.page.title = "XBot V2.1"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_resizable = True
        self.page.window_maximizable = True
        self.page.padding = 20
        self.page.bgcolor = "#1a1a1a"  # Dark theme

        # Load custom font
        self.page.fonts = {
            "Inter": "https://rsms.me/inter/font-files/Inter-Regular.otf?v=3.19"
        }
        self.page.theme = ft.Theme(font_family="Inter")

    # =========================================================================
    # BOOTSTRAP SCREEN (Identity Creation/Restoration)
    # =========================================================================

    def render_bootstrap(self):
        """
        Initial screen: Create or restore identity

        Layout:
        - Welcome message
        - Two tabs: "Create New" and "Restore Existing"
        - Input fields for CLIENT_ID and PASSWORD
        - Submit button
        """
        self.page.clean()

        # State
        create_mode = ft.Ref[bool]()
        create_mode.current = True

        # Input fields
        new_client_id = ft.TextField(
            label="CLIENT_ID",
            hint_text="Enter your client ID",
            width=400,
            password=False,
            bgcolor="#2a2a2a",
            border_color="#3a3a3a"
        )

        new_password = ft.TextField(
            label="PASSWORD",
            hint_text="Enter your password",
            width=400,
            password=True,
            can_reveal_password=True,
            bgcolor="#2a2a2a",
            border_color="#3a3a3a"
        )

        existing_client_id = ft.TextField(
            label="CLIENT_ID",
            hint_text="Your saved client ID",
            width=400,
            bgcolor="#2a2a2a",
            border_color="#3a3a3a"
        )

        existing_password = ft.TextField(
            label="PASSWORD",
            hint_text="Your saved password",
            width=400,
            password=True,
            can_reveal_password=True,
            bgcolor="#2a2a2a",
            border_color="#3a3a3a"
        )

        # Snackbar for messages
        def show_snackbar(message, color=ft.colors.GREEN):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=color
            )
            self.page.snack_bar.open = True
            self.page.update()

        # Submit handlers
        def submit_new(e):
            """Create new identity"""
            if not new_client_id.value or not new_password.value:
                show_snackbar("Please fill all fields", ft.colors.RED)
                return

            # Store credentials
            self.app.keyring.set_password(
                self.app.SERVICE_CLIENT_ID,
                "client_id",
                new_client_id.value
            )
            self.app.keyring.set_password(
                self.app.SERVICE_PASSWORD,
                "password",
                new_password.value
            )

            show_snackbar("Identity created successfully!")
            asyncio.sleep(1)
            self.render_main_dashboard()

        def submit_existing(e):
            """Restore existing identity"""
            if not existing_client_id.value or not existing_password.value:
                show_snackbar("Please fill all fields", ft.colors.RED)
                return

            # Verify credentials exist
            stored_id = self.app.keyring.get_password(
                self.app.SERVICE_CLIENT_ID,
                "client_id"
            )

            if stored_id:
                show_snackbar("Identity restored!")
                self.render_main_dashboard(restore=True)
            else:
                show_snackbar("Identity not found", ft.colors.RED)

        # Mode switcher
        def switch_mode(e):
            create_mode.current = not create_mode.current
            new_tab.visible = create_mode.current
            existing_tab.visible = not create_mode.current
            self.page.update()

        # Build tabs
        new_tab = ft.Column([
            ft.Text("Create New Identity", size=18, weight=ft.FontWeight.BOLD),
            new_client_id,
            new_password,
            ft.ElevatedButton(
                "Create Identity",
                on_click=submit_new,
                width=400,
                bgcolor=ft.colors.BLUE_700
            )
        ], visible=True)

        existing_tab = ft.Column([
            ft.Text("Restore Identity", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Use your saved credentials to recover your XBOT licenses.",
                   color=ft.colors.GREY_400),
            existing_client_id,
            existing_password,
            ft.ElevatedButton(
                "Restore Identity",
                on_click=submit_existing,
                width=400,
                bgcolor=ft.colors.GREEN_700
            )
        ], visible=False)

        # Close dialog handler
        def close_dialog(e):
            self.page.window_destroy()

        # Main layout
        self.page.add(
            ft.Container(
                content=ft.Column([
                    # Header
                    ft.Row([
                        ft.Text("Welcome to", size=36, weight=ft.FontWeight.W300),
                        ft.Text("XBOT", size=36, weight=ft.FontWeight.BOLD,
                               color=ft.colors.BLUE_400)
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Container(height=20),

                    # Warning message
                    ft.Container(
                        content=ft.Text(
                            "Please purchase from @PurchaseTwitterXBot on Telegram instead.",
                            size=12,
                            color=ft.colors.RED_400
                        ),
                        bgcolor=ft.colors.RED_900,
                        padding=10,
                        border_radius=5
                    ),

                    ft.Container(height=30),

                    # Mode toggle
                    ft.Row([
                        ft.TextButton("Create New", on_click=switch_mode),
                        ft.Text("or"),
                        ft.TextButton("Restore Existing", on_click=switch_mode)
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Container(height=20),

                    # Tab content
                    new_tab,
                    existing_tab,

                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        )

    # =========================================================================
    # MAIN DASHBOARD
    # =========================================================================

    def render_main_dashboard(self, restore=False):
        """
        Main dashboard screen

        Layout:
        - Top: Title and navigation
        - Left: Profile list with run/pause buttons
        - Center: Status indicators and controls
        - Right: License information
        - Bottom: Add profile and settings buttons
        """
        self.page.clean()

        # Profile list
        profile_list = ft.ListView(
            spacing=10,
            padding=10,
            expand=True
        )

        # Build rows for each profile
        for profile in self.app.profile_manager.profiles:
            row = self._build_profile_row(profile)
            profile_list.controls.append(row)

        # Empty state
        if not self.app.profile_manager.profiles:
            profile_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.ACCOUNT_CIRCLE_OUTLINED,
                               size=64, color=ft.colors.GREY_600),
                        ft.Text("No profiles added",
                               size=16, color=ft.colors.GREY_600),
                        ft.Text("Click 'Add Profile' to get started",
                               size=12, color=ft.colors.GREY_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=40
                )
            )

        # Main layout
        self.page.add(
            ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("XBOT Dashboard",
                               size=24, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.icons.LICENSE_OUTLINED,
                            tooltip="Manage Licenses",
                            on_click=self._show_license_management
                        ),
                        ft.IconButton(
                            icon=ft.icons.SETTINGS,
                            tooltip="Global Settings",
                            on_click=self._show_settings_dialog
                        )
                    ]),
                    padding=ft.padding.only(bottom=20)
                ),

                # Profile list
                ft.Container(
                    content=profile_list,
                    bgcolor="#2a2a2a",
                    border_radius=10,
                    padding=10,
                    expand=True
                ),

                # Action buttons
                ft.Row([
                    ft.ElevatedButton(
                        "Add Profile",
                        icon=ft.icons.ADD,
                        on_click=self._show_add_profile_dialog,
                        bgcolor=ft.colors.BLUE_700
                    ),
                    ft.ElevatedButton(
                        "Settings",
                        icon=ft.icons.TUNE,
                        on_click=self._show_settings_dialog,
                        bgcolor=ft.colors.GREEN_700
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], expand=True)
        )

        # Restore licenses if requested
        if restore:
            self._restore_licenses()

    def _build_profile_row(self, profile):
        """
        Build UI row for a single profile

        Layout:
        [Avatar] [Username] [Tag] [Status] [Run Button] [Settings] [Remove]
        """
        profile_id = profile['id']
        state = self.app.profile_manager.states.get(profile_id, {})

        # Status indicator
        status_text = ft.Text(
            "Idle",
            size=12,
            color=ft.colors.GREY_500
        )
        self.status_indicators[profile_id] = status_text

        # Progress indicator
        progress_bar = ft.ProgressBar(
            value=0,
            width=100,
            height=4,
            visible=False
        )
        self.progress_bars[profile_id] = progress_bar

        # Run/pause button
        async def on_run_click(e):
            if state.get('running'):
                # Stop
                await self.app._stop_profile(profile_id)
                run_button.text = "Run"
                run_button.icon = ft.icons.PLAY_ARROW
                run_button.bgcolor = ft.colors.GREEN_700
            else:
                # Start
                await self.app._start_profile(profile_id)
                run_button.text = "Stop"
                run_button.icon = ft.icons.STOP
                run_button.bgcolor = ft.colors.RED_700

            self.page.update()

        run_button = ft.ElevatedButton(
            "Run",
            icon=ft.icons.PLAY_ARROW,
            on_click=on_run_click,
            bgcolor=ft.colors.GREEN_700
        )

        # Settings button
        def on_settings_click(e):
            self._show_profile_settings_dialog(profile)

        # Remove button
        def on_remove_click(e):
            self._confirm_remove_profile(profile)

        # Build row
        return ft.Container(
            content=ft.Row([
                # Avatar
                ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=32),

                # Username and tag
                ft.Column([
                    ft.Text(f"@{profile['username']}",
                           weight=ft.FontWeight.BOLD),
                    ft.Text(profile.get('tag', ''),
                           size=10, color=ft.colors.GREY_500)
                ], spacing=2),

                # Spacer
                ft.Container(expand=True),

                # Status
                ft.Column([
                    status_text,
                    progress_bar
                ], horizontal_alignment=ft.CrossAxisAlignment.END),

                # Controls
                run_button,
                ft.IconButton(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    on_click=on_settings_click,
                    tooltip="Profile Settings"
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    on_click=on_remove_click,
                    tooltip="Remove Profile",
                    icon_color=ft.colors.RED_400
                )
            ], alignment=ft.MainAxisAlignment.START),
            bgcolor="#3a3a3a",
            padding=10,
            border_radius=5
        )

    # =========================================================================
    # ADD PROFILE DIALOG
    # =========================================================================

    def _show_add_profile_dialog(self, e):
        """Dialog to add new Twitter account profile"""

        username_field = ft.TextField(
            label="Twitter Username",
            hint_text="@username",
            prefix_text="@",
            width=400
        )

        email_field = ft.TextField(
            label="Email",
            hint_text="account@email.com",
            width=400
        )

        password_field = ft.TextField(
            label="Password",
            hint_text="Twitter password",
            password=True,
            can_reveal_password=True,
            width=400
        )

        license_field = ft.TextField(
            label="License Key (Optional)",
            hint_text="XXXX-XXXX-XXXX-XXXX",
            width=400
        )

        tag_field = ft.TextField(
            label="Profile Tag",
            hint_text="My Profile",
            width=400
        )

        def on_add(e):
            if not all([username_field.value, email_field.value,
                       password_field.value]):
                return

            # Add profile
            self.app.profile_manager.add_profile(
                username=username_field.value.lstrip('@'),
                email=email_field.value,
                password=password_field.value,
                license_key=license_field.value,
                tag=tag_field.value or username_field.value
            )

            dialog.open = False
            self.page.update()
            self.render_main_dashboard()  # Refresh

        def on_close(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add Twitter Account"),
            content=ft.Column([
                username_field,
                email_field,
                password_field,
                license_field,
                tag_field
            ], tight=True, height=400),
            actions=[
                ft.TextButton("Cancel", on_click=on_close),
                ft.ElevatedButton("Add Profile", on_click=on_add)
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # =========================================================================
    # SETTINGS DIALOG
    # =========================================================================

    def _show_settings_dialog(self, e):
        """
        Global settings configuration dialog

        Settings:
        - Drop Limit (slider)
        - Drop Sleep (slider)
        - Rate Limit Sleep (slider)
        - GIF Keyword (text)
        - Randomize (toggle)
        - No GIF (toggle)
        - Drop Message (multiline text)
        - Skip options (checkboxes)
        """
        settings = self.app.profile_manager.settings

        # Drop limit slider
        drop_limit_text = ft.Text(f"Drop Limit: {settings['drop_limit']}")
        drop_limit_slider = ft.Slider(
            min=1,
            max=100,
            value=settings['drop_limit'],
            divisions=99,
            label="{value}",
            on_change=lambda e: drop_limit_text.update()
        )

        # Drop sleep slider
        drop_sleep_text = ft.Text(f"Drop Sleep: {settings['drop_sleep']}s")
        drop_sleep_slider = ft.Slider(
            min=1,
            max=60,
            value=settings['drop_sleep'],
            divisions=59,
            label="{value}s",
            on_change=lambda e: drop_sleep_text.update()
        )

        # Rate limit sleep slider
        rate_limit_text = ft.Text(f"Rate Limit Sleep: {settings['rate_limit_sleep']}s")
        rate_limit_slider = ft.Slider(
            min=10,
            max=300,
            value=settings['rate_limit_sleep'],
            divisions=29,
            label="{value}s",
            on_change=lambda e: rate_limit_text.update()
        )

        # GIF keyword
        gif_keyword_field = ft.TextField(
            label="GIF Keyword",
            value=settings['gif_keyword'],
            hint_text="Search term for GIF",
            width=300
        )

        # Toggles
        randomize_toggle = ft.Switch(
            label="Randomize GIF Keyword",
            value=settings['randomize']
        )

        no_gif_toggle = ft.Switch(
            label="No GIF",
            value=settings['no_gif']
        )

        # Drop message
        drop_message_field = ft.TextField(
            label="Drop Message",
            value=settings['drop_message'],
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=400
        )

        # Skip options
        skip_followers = ft.Checkbox(
            label="Skip Missing Followers",
            value=settings['skip_missing_followers']
        )

        skip_chudai = ft.Checkbox(
            label="Skip Chudai",
            value=settings['skip_chudai']
        )

        skip_non_of = ft.Checkbox(
            label="Skip Non-OF Link",
            value=settings['skip_non_of_link']
        )

        # Save handler
        def save_settings(e):
            settings['drop_limit'] = int(drop_limit_slider.value)
            settings['drop_sleep'] = int(drop_sleep_slider.value)
            settings['rate_limit_sleep'] = int(rate_limit_slider.value)
            settings['gif_keyword'] = gif_keyword_field.value
            settings['randomize'] = randomize_toggle.value
            settings['no_gif'] = no_gif_toggle.value
            settings['drop_message'] = drop_message_field.value
            settings['skip_missing_followers'] = skip_followers.value
            settings['skip_chudai'] = skip_chudai.value
            settings['skip_non_of_link'] = skip_non_of.value

            self.app.profile_manager.save_settings()

            dialog.open = False
            self.page.update()

        def close_settings(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Bot Settings"),
            content=ft.Column([
                ft.Text("Drop Configuration", weight=ft.FontWeight.BOLD),
                drop_limit_text,
                drop_limit_slider,
                drop_sleep_text,
                drop_sleep_slider,
                rate_limit_text,
                rate_limit_slider,

                ft.Divider(),

                ft.Text("GIF Settings", weight=ft.FontWeight.BOLD),
                gif_keyword_field,
                randomize_toggle,
                no_gif_toggle,

                ft.Divider(),

                ft.Text("Message", weight=ft.FontWeight.BOLD),
                drop_message_field,

                ft.Divider(),

                ft.Text("Skip Options", weight=ft.FontWeight.BOLD),
                skip_followers,
                skip_chudai,
                skip_non_of,

            ], tight=True, scroll=ft.ScrollMode.AUTO, height=600),
            actions=[
                ft.TextButton("Cancel", on_click=close_settings),
                ft.ElevatedButton("Save", on_click=save_settings)
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    # =========================================================================
    # LICENSE MANAGEMENT
    # =========================================================================

    def _show_license_management(self, e):
        """Show license key management screen"""

        # This would show license entry/validation UI
        # In cracked version, bypassed
        pass

    def _restore_licenses(self):
        """Restore licenses from saved data"""
        # Load licenses from profiles
        pass

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _confirm_remove_profile(self, profile):
        """Confirm profile deletion"""
        def do_remove(e):
            self.app.profile_manager.profiles.remove(profile)
            self.app.profile_manager.save_profiles()
            dialog.open = False
            self.page.update()
            self.render_main_dashboard()

        def cancel(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Remove Profile?"),
            content=ft.Text(f"Are you sure you want to remove @{profile['username']}?"),
            actions=[
                ft.TextButton("Cancel", on_click=cancel),
                ft.ElevatedButton("Remove", on_click=do_remove, bgcolor=ft.colors.RED_700)
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def update_status(self, profile_id, status_text, progress=None):
        """Update status indicator for a profile"""
        if profile_id in self.status_indicators:
            self.status_indicators[profile_id].value = status_text

        if profile_id in self.progress_bars and progress is not None:
            self.progress_bars[profile_id].value = progress
            self.progress_bars[profile_id].visible = True

        self.page.update()
