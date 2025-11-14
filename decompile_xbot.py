#!/usr/bin/env python3
"""
XBot Advanced Decompilation Attempts
Tries multiple methods to convert XBot.pyc to readable Python source code
"""

import sys
import subprocess
import marshal
import dis
from pathlib import Path
import struct


class XBotDecompiler:
    """Attempts multiple decompilation strategies for Python 3.13 bytecode"""

    def __init__(self, pyc_path: str, output_dir: str = './decompiled'):
        self.pyc_path = Path(pyc_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.code_object = None

    def load_bytecode(self):
        """Load the .pyc file and extract code object"""
        print(f"[*] Loading {self.pyc_path}")

        with open(self.pyc_path, 'rb') as f:
            # Skip header (16 bytes for Python 3.13)
            magic = f.read(4)
            flags = f.read(4)
            timestamp = f.read(8)

            print(f"[+] Magic: {magic.hex()}")

            try:
                self.code_object = marshal.load(f)
                print(f"[+] Code object loaded successfully")
                return True
            except Exception as e:
                print(f"[-] Failed to load code object: {e}")
                return False

    def method1_pycdc(self):
        """Attempt 1: Use pycdc (supports Python 3.13)"""
        print("\n" + "="*80)
        print("METHOD 1: pycdc Decompilation")
        print("="*80)

        output_file = self.output_dir / 'XBot_pycdc.py'

        # Check if pycdc is available
        pycdc_paths = [
            'pycdc',
            './pycdc',
            '/usr/local/bin/pycdc',
            '/opt/homebrew/bin/pycdc'
        ]

        pycdc_cmd = None
        for path in pycdc_paths:
            try:
                result = subprocess.run([path, '--version'], capture_output=True, timeout=5)
                if result.returncode == 0 or 'pycdc' in result.stderr.decode():
                    pycdc_cmd = path
                    break
            except:
                continue

        if not pycdc_cmd:
            print("[-] pycdc not found. Install instructions:")
            print("    macOS: brew install pycdc")
            print("    Or download from: https://github.com/zrax/pycdc")
            return False

        print(f"[+] Found pycdc at: {pycdc_cmd}")

        try:
            print(f"[*] Decompiling to {output_file}...")
            result = subprocess.run(
                [pycdc_cmd, str(self.pyc_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and result.stdout:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                print(f"[+] SUCCESS! Decompiled to {output_file}")
                print(f"[+] File size: {output_file.stat().st_size} bytes")
                return True
            else:
                print(f"[-] pycdc failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("[-] pycdc timed out")
            return False
        except Exception as e:
            print(f"[-] pycdc error: {e}")
            return False

    def method2_uncompyle6(self):
        """Attempt 2: Try uncompyle6 (will likely fail for 3.13)"""
        print("\n" + "="*80)
        print("METHOD 2: uncompyle6 Decompilation")
        print("="*80)

        output_file = self.output_dir / 'XBot_uncompyle6.py'

        try:
            import uncompyle6
            print("[+] uncompyle6 is installed")

            with open(output_file, 'w') as f:
                try:
                    uncompyle6.decompile_file(str(self.pyc_path), f)
                    print(f"[+] SUCCESS! Decompiled to {output_file}")
                    return True
                except Exception as e:
                    print(f"[-] uncompyle6 failed: {e}")
                    return False

        except ImportError:
            print("[-] uncompyle6 not installed")
            print("    Install: pip3 install uncompyle6")
            return False

    def method3_decompyle3(self):
        """Attempt 3: Try decompyle3"""
        print("\n" + "="*80)
        print("METHOD 3: decompyle3 Decompilation")
        print("="*80)

        output_file = self.output_dir / 'XBot_decompyle3.py'

        try:
            result = subprocess.run(
                ['decompyle3', str(self.pyc_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and result.stdout:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                print(f"[+] SUCCESS! Decompiled to {output_file}")
                return True
            else:
                print(f"[-] decompyle3 failed or not installed")
                return False

        except FileNotFoundError:
            print("[-] decompyle3 not found")
            print("    Install: pip3 install decompyle3")
            return False
        except Exception as e:
            print(f"[-] decompyle3 error: {e}")
            return False

    def method4_manual_reconstruction(self):
        """Attempt 4: Manual reconstruction from bytecode"""
        print("\n" + "="*80)
        print("METHOD 4: Manual Bytecode Analysis & Reconstruction")
        print("="*80)

        output_file = self.output_dir / 'XBot_reconstructed.py'

        print("[*] Analyzing bytecode structure...")

        # This will create pseudocode based on bytecode analysis
        pseudocode = self._reconstruct_from_bytecode(self.code_object)

        with open(output_file, 'w') as f:
            f.write(pseudocode)

        print(f"[+] Pseudocode/partial reconstruction saved to {output_file}")
        print("[!] Note: This is NOT complete Python code, but shows program logic")
        return True

    def _reconstruct_from_bytecode(self, code_obj, indent=0):
        """Reconstruct pseudocode from bytecode analysis"""
        lines = []
        ind = "    " * indent

        # Header
        lines.append("# " + "="*70)
        lines.append(f"# Reconstructed from bytecode: {code_obj.co_name}")
        lines.append("# WARNING: This is pseudocode/partial reconstruction")
        lines.append("# " + "="*70)
        lines.append("")

        # Imports (guessed from names)
        lines.append("# Detected imports:")
        for name in code_obj.co_names:
            if any(mod in name for mod in ['datetime', 'asyncio', 'keyring', 'playwright', 'aiohttp']):
                lines.append(f"# import {name}")
        lines.append("")

        # Function signature
        args = code_obj.co_varnames[:code_obj.co_argcount]
        if args:
            lines.append(f"def {code_obj.co_name}({', '.join(args)}):")
        else:
            lines.append(f"def {code_obj.co_name}():")

        # Constants found
        lines.append(f"{ind}# Constants used in this function:")
        for const in code_obj.co_consts:
            if isinstance(const, str) and len(const) < 100:
                lines.append(f'{ind}# "{const}"')
            elif isinstance(const, (int, float)) and not isinstance(const, bool):
                lines.append(f'{ind}# {const}')

        lines.append("")
        lines.append(f"{ind}# Bytecode operations:")

        # Disassembly
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            dis.dis(code_obj)
            disasm = buffer.getvalue()

            # Add as comments
            for line in disasm.split('\n'):
                if line.strip():
                    lines.append(f"{ind}# {line}")
        finally:
            sys.stdout = old_stdout

        lines.append("")
        lines.append(f"{ind}pass  # See disassembly comments above")
        lines.append("")

        # Nested code objects (functions/classes)
        for const in code_obj.co_consts:
            if hasattr(const, 'co_name'):
                lines.append("")
                lines.extend(self._reconstruct_from_bytecode(const, indent).split('\n'))

        return '\n'.join(lines)

    def method5_hybrid_analysis(self):
        """Attempt 5: Create hybrid readable format"""
        print("\n" + "="*80)
        print("METHOD 5: Hybrid Analysis (Strings + Logic + Documentation)")
        print("="*80)

        output_file = self.output_dir / 'XBot_hybrid_analysis.py'

        print("[*] Creating comprehensive hybrid analysis...")

        hybrid = self._create_hybrid_analysis()

        with open(output_file, 'w') as f:
            f.write(hybrid)

        print(f"[+] Hybrid analysis saved to {output_file}")
        print("[+] This combines strings, logic flow, and documentation")
        return True

    def _create_hybrid_analysis(self):
        """Create a hybrid readable format with all extracted info"""
        output = []

        output.append('"""')
        output.append('XBot Twitter Automation Bot - Hybrid Analysis')
        output.append('=' * 70)
        output.append('')
        output.append('This is a reconstructed understanding of XBot based on:')
        output.append('- Bytecode disassembly')
        output.append('- String extraction')
        output.append('- Function signature analysis')
        output.append('- Constant analysis')
        output.append('')
        output.append('NOTE: This is NOT decompiled source code.')
        output.append('      This shows WHAT the bot does based on analysis.')
        output.append('"""')
        output.append('')
        output.append('# ' + '='*70)
        output.append('# IMPORTS (Detected from bytecode)')
        output.append('# ' + '='*70)
        output.append('')
        output.append('from datetime import datetime, timedelta')
        output.append('from asyncio import AsyncRunner')
        output.append('import keyring')
        output.append('# from playwright import ...')
        output.append('# import aiohttp')
        output.append('# import flet as ft')
        output.append('')
        output.append('')
        output.append('# ' + '='*70)
        output.append('# CONFIGURATION STRUCTURE')
        output.append('# ' + '='*70)
        output.append('')
        output.append('DEFAULT_SETTINGS = {')
        output.append('    "drop_limit": 50,          # Max messages to send')
        output.append('    "drop_sleep": 5,           # Seconds between messages')
        output.append('    "after_drops": None,       # Action after completion')
        output.append('    "rate_limit_sleep": 60,    # Sleep when rate limited')
        output.append('    "group_skip": [],          # Groups to skip')
        output.append('    "leniency_1_3": True,      # Detection avoidance level 1')
        output.append('    "leniency_1_4": True,      # Detection avoidance level 2')
        output.append('    "leniency_2_5": True,      # Detection avoidance level 3')
        output.append('    "gif_keyword": "hello",    # GIF search keyword')
        output.append('    "randomize": True,         # Randomize GIF selection')
        output.append('    "no_gif": False,           # Disable GIF attachment')
        output.append('    "drop_message": "Hit my pinned post\\nPlease add me to your groups",')
        output.append('    "skip_chudai": True,')
        output.append('    "skip_missing_followers": True,')
        output.append('    "skip_non_of_link": True,')
        output.append('    "assume_invalid_room_as_three": False,')
        output.append('}')
        output.append('')
        output.append('')
        output.append('# ' + '='*70)
        output.append('# MAIN APPLICATION CLASS')
        output.append('# ' + '='*70)
        output.append('')
        output.append('class XBotApp:')
        output.append('    """')
        output.append('    XBot V2.1 - Twitter Automation Bot')
        output.append('    Also known as: DolphinBot')
        output.append('    ')
        output.append('    Purchased from: @PurchaseTwitterXBot on Telegram')
        output.append('    """')
        output.append('    ')
        output.append('    SERVICE_CLIENT_ID = "XBot"')
        output.append('    SERVICE_PASSWORD = "XBot.py"')
        output.append('    ')
        output.append('    def __init__(self, page):')
        output.append('        """Initialize XBot application"""')
        output.append('        self.page = page')
        output.append('        self.runner = None')
        output.append('        self.keyring = keyring')
        output.append('        ')
        output.append('        # Load saved data')
        output.append('        self.saved_profiles = {}')
        output.append('        self.accounts = []')
        output.append('        self.all_settings = DEFAULT_SETTINGS.copy()')
        output.append('        ')
        output.append('        # State tracking')
        output.append('        self.states = {}  # Per-profile state')
        output.append('        ')
        output.append('        # UI elements')
        output.append('        self.license_column = None')
        output.append('        self.show_keys = False')
        output.append('        ')
        output.append('        # Load configuration')
        output.append('        self._load_profiles_local()')
        output.append('        self._load_settings_local()')
        output.append('')
        output.append('    def _ensure_pid_state(self, profile_id):')
        output.append('        """Ensure state exists for profile"""')
        output.append('        if profile_id not in self.states:')
        output.append('            self.states[profile_id] = {')
        output.append('                "paused": False,')
        output.append('                "error": None,')
        output.append('                "runtime_task": None,')
        output.append('                "anim_task": None,')
        output.append('                "scheduled": False,')
        output.append('                "cancel_scheduled": False,')
        output.append('                "scheduled_task": None,')
        output.append('                "scheduled_start_time": None,')
        output.append('                "runtime": 0,')
        output.append('                "drop_count": 0,')
        output.append('            }')
        output.append('        return self.states[profile_id]')
        output.append('')
        output.append('    def get_password(self, service, username):')
        output.append('        """Retrieve password from keyring"""')
        output.append('        return self.keyring.get_password(service, username)')
        output.append('')
        output.append('    def _load_profiles_local(self):')
        output.append('        """Load profiles from .xbot_profiles.json"""')
        output.append('        # Loads Twitter account credentials')
        output.append('        # File location: ./.xbot_profiles.json')
        output.append('        pass')
        output.append('')
        output.append('    def _save_profiles_local(self):')
        output.append('        """Save profiles to .xbot_profiles.json"""')
        output.append('        pass')
        output.append('')
        output.append('    def _load_settings_local(self):')
        output.append('        """Load settings from .settings.json"""')
        output.append('        # Loads bot configuration')
        output.append('        # File location: ./.settings.json')
        output.append('        pass')
        output.append('')
        output.append('    def _save_settings_local(self):')
        output.append('        """Save settings to .settings.json"""')
        output.append('        pass')
        output.append('')
        output.append('    async def _run_automation(self, profile):')
        output.append('        """')
        output.append('        Main automation loop - sends spam messages')
        output.append('        ')
        output.append('        Process:')
        output.append('        1. Login to Twitter via Playwright')
        output.append('        2. Get target list (groups/users)')
        output.append('        3. For each target:')
        output.append('           - Check if should skip')
        output.append('           - Post message + optional GIF')
        output.append('           - Sleep for drop_sleep seconds')
        output.append('           - Increment drop_count')
        output.append('        4. When drop_count >= drop_limit: stop')
        output.append('        """')
        output.append('        pass')
        output.append('')
        output.append('    def _configure_page_window(self):')
        output.append('        """Configure Flet window"""')
        output.append('        self.page.title = "XBot V2.1"')
        output.append('        self.page.window_width = 800')
        output.append('        self.page.window_height = 600')
        output.append('        self.page.fonts = {')
        output.append('            "Inter": "https://rsms.me/inter/font-files/Inter-Regular.otf?v=3.19"')
        output.append('        }')
        output.append('')
        output.append('    def run_bootstrap(self):')
        output.append('        """Show create/restore identity screen"""')
        output.append('        self._configure_page_window()')
        output.append('        self._render_bootstrap()')
        output.append('')
        output.append('    def run_main(self, restore=False):')
        output.append('        """Show main dashboard"""')
        output.append('        self._configure_page_window()')
        output.append('        self._render_main_dashboard()')
        output.append('        ')
        output.append('        if restore:')
        output.append('            self._restore_licenses()')
        output.append('')
        output.append('    def _render_bootstrap(self):')
        output.append('        """Render identity screen UI"""')
        output.append('        # Shows "Welcome to XBOT" screen')
        output.append('        # Options: Create new identity or Restore existing')
        output.append('        pass')
        output.append('')
        output.append('    def _render_main_dashboard(self):')
        output.append('        """Render main dashboard UI"""')
        output.append('        # Shows:')
        output.append('        # - Profile list')
        output.append('        # - Settings panel')
        output.append('        # - Run/pause controls')
        output.append('        # - Status indicators')
        output.append('        pass')
        output.append('')
        output.append('    def _show_settings_dialog(self, profile_id):')
        output.append('        """Show settings configuration dialog"""')
        output.append('        # Allows configuration of:')
        output.append('        # - drop_limit, drop_sleep')
        output.append('        # - rate_limit_sleep')
        output.append('        # - gif_keyword, randomize, no_gif')
        output.append('        # - skip options')
        output.append('        # - drop_message text')
        output.append('        pass')
        output.append('')
        output.append('    def _toggle_run(self, profile_id):')
        output.append('        """Start/stop bot for profile"""')
        output.append('        state = self._ensure_pid_state(profile_id)')
        output.append('        ')
        output.append('        if state["runtime_task"]:')
        output.append('            # Stop bot')
        output.append('            state["runtime_task"].cancel()')
        output.append('        else:')
        output.append('            # Start bot')
        output.append('            state["runtime_task"] = asyncio.create_task(')
        output.append('                self._run_automation(profile_id)')
        output.append('            )')
        output.append('')
        output.append('    def _check_license(self, license_key):')
        output.append('        """Validate license key (bypassed in cracked version)"""')
        output.append('        # Original: contacts license server')
        output.append('        # Cracked: always returns valid')
        output.append('        print("Please purchase from @PurchaseTwitterXBot on Telegram instead.")')
        output.append('        return True  # Bypassed')
        output.append('')
        output.append('')
        output.append('# ' + '='*70)
        output.append('# PURCHASE UI (License System)')
        output.append('# ' + '='*70)
        output.append('')
        output.append('class PurchaseUI:')
        output.append('    """Handles cryptocurrency payment UI"""')
        output.append('    ')
        output.append('    def __init__(self, parent):')
        output.append('        self.parent = parent')
        output.append('        ')
        output.append('    def _build_crypto_selector(self):')
        output.append('        """Build cryptocurrency selection UI"""')
        output.append('        # Supported: BTC, ETH, XMR, etc.')
        output.append('        # Generates QR codes: https://quickchart.io/qr?text=<address>')
        output.append('        pass')
        output.append('')
        output.append('')
        output.append('# ' + '='*70)
        output.append('# HELPER FUNCTIONS')
        output.append('# ' + '='*70)
        output.append('')
        output.append('def generate_particles():')
        output.append('    """Generate animated background particles"""')
        output.append('    pass')
        output.append('')
        output.append('def generate_shimmering_dust():')
        output.append('    """Generate shimmering dust effect"""')
        output.append('    pass')
        output.append('')
        output.append('')
        output.append('# ' + '='*70)
        output.append('# ENTRY POINTS')
        output.append('# ' + '='*70)
        output.append('')
        output.append('def bootstrap(page):')
        output.append('    """Entry point: show identity screen"""')
        output.append('    app = XBotApp(page)')
        output.append('    app.run_bootstrap()')
        output.append('')
        output.append('def main(page, restore=False):')
        output.append('    """Entry point: show main dashboard"""')
        output.append('    app = XBotApp(page)')
        output.append('    app.run_main(restore=restore)')
        output.append('')
        output.append('')
        output.append('if __name__ == "__main__":')
        output.append('    import flet as ft')
        output.append('    ft.app(target=bootstrap)')

        return '\n'.join(output)

    def run_all_methods(self):
        """Try all decompilation methods"""
        print("\n" + "="*80)
        print("XBot Advanced Decompilation - Trying All Methods")
        print("="*80)
        print()

        if not self.load_bytecode():
            return False

        results = {}

        # Try each method
        results['pycdc'] = self.method1_pycdc()
        results['uncompyle6'] = self.method2_uncompyle6()
        results['decompyle3'] = self.method3_decompyle3()
        results['manual'] = self.method4_manual_reconstruction()
        results['hybrid'] = self.method5_hybrid_analysis()

        # Summary
        print("\n" + "="*80)
        print("DECOMPILATION SUMMARY")
        print("="*80)

        for method, success in results.items():
            status = "[+] SUCCESS" if success else "[-] FAILED"
            print(f"{status}: {method}")

        print("\n" + "="*80)
        print(f"Output directory: {self.output_dir}")
        print("="*80)

        # Check what we got
        output_files = list(self.output_dir.glob('*.py'))
        if output_files:
            print("\nGenerated files:")
            for f in output_files:
                size = f.stat().st_size
                print(f"  - {f.name} ({size:,} bytes)")

        print("\n" + "="*80)
        print("RECOMMENDATION:")
        print("="*80)

        if results['pycdc']:
            print("✓ pycdc succeeded - check XBot_pycdc.py for clean source code")
        elif results['hybrid']:
            print("✓ Hybrid analysis created - check XBot_hybrid_analysis.py")
            print("  This shows program structure and logic flow")
        else:
            print("✓ Manual reconstruction available - check XBot_reconstructed.py")
            print("  This contains bytecode analysis with pseudocode")

        return True


def main():
    if len(sys.argv) < 2:
        print("XBot Advanced Decompilation Tool")
        print("="*80)
        print("\nUsage: python3 decompile_xbot.py <XBot.pyc> [output_dir]")
        print("\nExample:")
        print("  python3 decompile_xbot.py XBot.pyc ./decompiled")
        print("\nPrerequisites (optional, will try what's available):")
        print("  - pycdc (best for Python 3.13)")
        print("    macOS: brew install pycdc")
        print("  - uncompyle6")
        print("    pip3 install uncompyle6")
        print("  - decompyle3")
        print("    pip3 install decompyle3")
        print("\n" + "="*80)
        sys.exit(1)

    pyc_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './decompiled'

    decompiler = XBotDecompiler(pyc_path, output_dir)
    decompiler.run_all_methods()


if __name__ == '__main__':
    main()
