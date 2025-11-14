#!/usr/bin/env python3
"""
XBot.pyc Bytecode Analysis Script
Extracts detailed information from Python 3.13 bytecode without decompiling
Author: Security Research
Purpose: Educational malware analysis
"""

import sys
import marshal
import dis
import struct
from pathlib import Path
from typing import Dict, List, Any
import json


class XBotBytecodeAnalyzer:
    """Analyzes XBot.pyc bytecode to extract functionality and IOCs"""

    def __init__(self, pyc_path: str):
        self.pyc_path = Path(pyc_path)
        self.code_object = None
        self.strings = []
        self.names = []
        self.consts = []
        self.imports = []
        self.functions = []

    def load_pyc(self):
        """Load and parse the .pyc file"""
        print(f"[*] Loading {self.pyc_path}")

        with open(self.pyc_path, 'rb') as f:
            # Python 3.13 .pyc header:
            # - Magic number (4 bytes)
            # - Flags (4 bytes)
            # - Timestamp/hash (8 bytes)
            magic = f.read(4)
            flags = f.read(4)
            timestamp_or_hash = f.read(8)

            print(f"[+] Magic: {magic.hex()}")
            print(f"[+] Flags: {flags.hex()}")
            print(f"[+] Timestamp/Hash: {timestamp_or_hash.hex()}")

            try:
                self.code_object = marshal.load(f)
                print(f"[+] Successfully loaded code object")
                return True
            except Exception as e:
                print(f"[-] Error loading code object: {e}")
                return False

    def extract_strings(self, code_obj=None):
        """Recursively extract all strings from code objects"""
        if code_obj is None:
            code_obj = self.code_object

        if not hasattr(code_obj, 'co_consts'):
            return

        for const in code_obj.co_consts:
            if isinstance(const, str):
                self.strings.append(const)
            elif hasattr(const, 'co_consts'):
                # Nested code object (function/class)
                self.extract_strings(const)

    def extract_names(self, code_obj=None):
        """Extract variable and function names"""
        if code_obj is None:
            code_obj = self.code_object

        if hasattr(code_obj, 'co_names'):
            self.names.extend(code_obj.co_names)

        if hasattr(code_obj, 'co_consts'):
            for const in code_obj.co_consts:
                if hasattr(const, 'co_names'):
                    self.extract_names(const)

    def extract_imports(self):
        """Identify imported modules from names"""
        import_keywords = ['import', 'from']

        # Common malware-relevant imports
        suspicious_modules = [
            'requests', 'urllib', 'socket', 'subprocess', 'os',
            'keyring', 'playwright', 'selenium', 'psutil',
            'win32api', 'win32con', 'ctypes', 'cryptography',
            'discord', 'telegram', 'aiohttp', 'asyncio'
        ]

        for name in self.names:
            if any(mod in name.lower() for mod in suspicious_modules):
                self.imports.append(name)

    def extract_constants(self, code_obj=None):
        """Extract all constants"""
        if code_obj is None:
            code_obj = self.code_object

        if hasattr(code_obj, 'co_consts'):
            for const in code_obj.co_consts:
                if isinstance(const, (str, int, float, bytes, tuple)):
                    self.consts.append(const)
                elif hasattr(const, 'co_consts'):
                    self.extract_constants(const)

    def find_urls(self):
        """Extract URLs and domains from strings"""
        urls = []
        domains = []

        for s in self.strings:
            if isinstance(s, str):
                # URLs
                if 'http://' in s or 'https://' in s:
                    urls.append(s)
                # Domains
                if '.com' in s or '.net' in s or '.io' in s or '.org' in s or '.gg' in s:
                    domains.append(s)

        return urls, domains

    def find_credentials(self):
        """Find potential credential-related strings"""
        cred_keywords = [
            'password', 'passwd', 'pwd', 'token', 'api_key', 'apikey',
            'secret', 'auth', 'credential', 'login', 'username', 'user',
            'client_id', 'client_secret', 'bearer', 'authorization'
        ]

        creds = []
        for s in self.strings:
            if isinstance(s, str):
                if any(kw in s.lower() for kw in cred_keywords):
                    creds.append(s)

        return creds

    def find_file_operations(self):
        """Find file paths and operations"""
        file_ops = []

        for name in self.names:
            if any(op in name.lower() for op in ['open', 'read', 'write', 'file', 'path']):
                file_ops.append(name)

        # Look for file paths in strings
        paths = []
        for s in self.strings:
            if isinstance(s, str):
                if any(indicator in s for indicator in ['.json', '.txt', '.log', '.db', '\\', '/']):
                    paths.append(s)

        return file_ops, paths

    def analyze_functions(self, code_obj=None, depth=0):
        """Recursively analyze function definitions"""
        if code_obj is None:
            code_obj = self.code_object

        if hasattr(code_obj, 'co_name'):
            func_info = {
                'name': code_obj.co_name,
                'argcount': code_obj.co_argcount if hasattr(code_obj, 'co_argcount') else 0,
                'names': list(code_obj.co_names) if hasattr(code_obj, 'co_names') else [],
                'depth': depth
            }
            self.functions.append(func_info)

        # Recurse into nested code objects
        if hasattr(code_obj, 'co_consts'):
            for const in code_obj.co_consts:
                if hasattr(const, 'co_name'):
                    self.analyze_functions(const, depth + 1)

    def disassemble_to_file(self, output_path: str):
        """Disassemble bytecode to file"""
        print(f"[*] Disassembling to {output_path}")

        with open(output_path, 'w') as f:
            sys.stdout = f
            dis.dis(self.code_object)
            sys.stdout = sys.__stdout__

        print(f"[+] Disassembly saved to {output_path}")

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        urls, domains = self.find_urls()
        creds = self.find_credentials()
        file_ops, paths = self.find_file_operations()

        report = {
            'metadata': {
                'file': str(self.pyc_path),
                'total_strings': len(self.strings),
                'total_names': len(self.names),
                'total_functions': len(self.functions),
                'total_imports': len(self.imports)
            },
            'urls': urls,
            'domains': domains,
            'credentials': creds,
            'file_operations': file_ops,
            'file_paths': paths,
            'imports': list(set(self.imports)),
            'suspicious_strings': self._find_suspicious_strings(),
            'functions': self.functions[:50],  # Top 50 functions
            'interesting_names': self._find_interesting_names()
        }

        return report

    def _find_suspicious_strings(self):
        """Find strings that indicate malicious behavior"""
        suspicious_keywords = [
            'bot', 'spam', 'drop', 'steal', 'grab', 'credential',
            'keylog', 'screenshot', 'webhook', 'discord', 'telegram',
            'license', 'crack', 'bypass', 'admin', 'elevate',
            'inject', 'payload', 'exploit', 'shell', 'backdoor'
        ]

        suspicious = []
        for s in self.strings:
            if isinstance(s, str) and len(s) > 3:
                if any(kw in s.lower() for kw in suspicious_keywords):
                    suspicious.append(s)

        return suspicious[:100]  # Top 100

    def _find_interesting_names(self):
        """Find interesting variable/function names"""
        interesting = []
        keywords = [
            'password', 'token', 'key', 'secret', 'auth',
            'drop', 'spam', 'bot', 'run', 'execute', 'inject'
        ]

        unique_names = list(set(self.names))
        for name in unique_names:
            if any(kw in name.lower() for kw in keywords):
                interesting.append(name)

        return interesting

    def run_analysis(self, output_dir: str = '.'):
        """Run complete analysis pipeline"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        print("[*] Starting XBot bytecode analysis...")

        # Load the .pyc file
        if not self.load_pyc():
            return False

        # Extract all data
        print("[*] Extracting strings...")
        self.extract_strings()
        print(f"[+] Found {len(self.strings)} strings")

        print("[*] Extracting names...")
        self.extract_names()
        print(f"[+] Found {len(self.names)} names")

        print("[*] Extracting constants...")
        self.extract_constants()
        print(f"[+] Found {len(self.consts)} constants")

        print("[*] Analyzing functions...")
        self.analyze_functions()
        print(f"[+] Found {len(self.functions)} functions")

        print("[*] Identifying imports...")
        self.extract_imports()
        print(f"[+] Found {len(self.imports)} imports")

        # Generate outputs
        print("[*] Generating disassembly...")
        self.disassemble_to_file(output_dir / 'XBot_disassembly.txt')

        print("[*] Generating analysis report...")
        report = self.generate_report()

        # Save report as JSON
        with open(output_dir / 'XBot_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print(f"[+] Report saved to {output_dir / 'XBot_analysis_report.json'}")

        # Save human-readable report
        self._save_readable_report(report, output_dir / 'XBot_analysis_report.txt')

        # Save extracted strings
        with open(output_dir / 'XBot_strings.txt', 'w') as f:
            for s in self.strings:
                if isinstance(s, str):
                    f.write(f"{s}\n")
        print(f"[+] Strings saved to {output_dir / 'XBot_strings.txt'}")

        print("\n[+] Analysis complete!")
        return True

    def _save_readable_report(self, report: Dict, output_path: Path):
        """Save human-readable analysis report"""
        with open(output_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("XBot Malware Analysis Report\n")
            f.write("=" * 80 + "\n\n")

            f.write("## METADATA\n")
            f.write("-" * 80 + "\n")
            for key, value in report['metadata'].items():
                f.write(f"{key}: {value}\n")

            f.write("\n## URLS FOUND\n")
            f.write("-" * 80 + "\n")
            for url in report['urls']:
                f.write(f"{url}\n")

            f.write("\n## DOMAINS FOUND\n")
            f.write("-" * 80 + "\n")
            for domain in report['domains']:
                f.write(f"{domain}\n")

            f.write("\n## CREDENTIAL-RELATED STRINGS\n")
            f.write("-" * 80 + "\n")
            for cred in report['credentials']:
                f.write(f"{cred}\n")

            f.write("\n## FILE PATHS\n")
            f.write("-" * 80 + "\n")
            for path in report['file_paths']:
                f.write(f"{path}\n")

            f.write("\n## SUSPICIOUS IMPORTS\n")
            f.write("-" * 80 + "\n")
            for imp in report['imports']:
                f.write(f"{imp}\n")

            f.write("\n## SUSPICIOUS STRINGS\n")
            f.write("-" * 80 + "\n")
            for s in report['suspicious_strings']:
                f.write(f"{s}\n")

            f.write("\n## INTERESTING NAMES\n")
            f.write("-" * 80 + "\n")
            for name in report['interesting_names']:
                f.write(f"{name}\n")

            f.write("\n## TOP FUNCTIONS\n")
            f.write("-" * 80 + "\n")
            for func in report['functions'][:30]:
                indent = "  " * func['depth']
                f.write(f"{indent}{func['name']} (args: {func['argcount']})\n")

        print(f"[+] Human-readable report saved to {output_path}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_xbot_bytecode.py <path_to_XBot.pyc> [output_dir]")
        print("\nExample:")
        print("  python3 analyze_xbot_bytecode.py XBot.pyc .")
        print("  python3 analyze_xbot_bytecode.py XBot.exe_extracted/XBot.pyc ./analysis")
        sys.exit(1)

    pyc_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './xbot_analysis'

    analyzer = XBotBytecodeAnalyzer(pyc_path)
    analyzer.run_analysis(output_dir)


if __name__ == '__main__':
    main()
