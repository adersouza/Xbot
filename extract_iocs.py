#!/usr/bin/env python3
"""
XBot IOC (Indicators of Compromise) Extractor
Extracts all observable artifacts from the malware for threat intelligence
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Set
import sys


class IOCExtractor:
    """Extract IOCs from XBot malware for detection and threat intel"""

    def __init__(self, strings_file: str, analysis_dir: str = None):
        self.strings_file = Path(strings_file)
        self.analysis_dir = Path(analysis_dir) if analysis_dir else self.strings_file.parent
        self.strings = []
        self.iocs = {
            'urls': [],
            'domains': [],
            'ips': [],
            'file_paths': [],
            'registry_keys': [],
            'mutexes': [],
            'user_agents': [],
            'api_endpoints': [],
            'email_addresses': [],
            'cryptocurrency_addresses': [],
            'telegram_handles': [],
            'discord_webhooks': [],
            'suspicious_strings': [],
            'file_hashes': {}
        }

    def load_strings(self):
        """Load strings from file"""
        print(f"[*] Loading strings from {self.strings_file}")
        with open(self.strings_file, 'r', encoding='utf-8', errors='ignore') as f:
            self.strings = [line.strip() for line in f if line.strip()]
        print(f"[+] Loaded {len(self.strings)} strings")

    def extract_urls(self):
        """Extract URLs"""
        url_pattern = re.compile(
            r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'
            r'(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        )

        for s in self.strings:
            matches = url_pattern.findall(s)
            self.iocs['urls'].extend(matches)

        self.iocs['urls'] = list(set(self.iocs['urls']))
        print(f"[+] Found {len(self.iocs['urls'])} unique URLs")

    def extract_domains(self):
        """Extract domain names"""
        domain_pattern = re.compile(
            r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
        )

        for s in self.strings:
            matches = domain_pattern.findall(s)
            for match in matches:
                # Filter out common false positives
                if not any(fp in match for fp in ['.py', '.pyc', '.json', '.txt', '.exe']):
                    self.iocs['domains'].append(match)

        self.iocs['domains'] = list(set(self.iocs['domains']))
        print(f"[+] Found {len(self.iocs['domains'])} unique domains")

    def extract_ips(self):
        """Extract IP addresses"""
        ip_pattern = re.compile(
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        )

        for s in self.strings:
            matches = ip_pattern.findall(s)
            self.iocs['ips'].extend(matches)

        self.iocs['ips'] = list(set(self.iocs['ips']))
        print(f"[+] Found {len(self.iocs['ips'])} unique IP addresses")

    def extract_file_paths(self):
        """Extract Windows and Unix file paths"""
        # Windows paths
        win_path_pattern = re.compile(r'[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*')
        # Unix paths
        unix_path_pattern = re.compile(r'(?:/[^/\0]+)+/?')
        # Relative paths with . or ..
        rel_path_pattern = re.compile(r'\.{1,2}[/\\][^\s]+')

        for s in self.strings:
            # Windows
            matches = win_path_pattern.findall(s)
            self.iocs['file_paths'].extend(matches)

            # Unix (filter to reasonable length)
            matches = unix_path_pattern.findall(s)
            self.iocs['file_paths'].extend([m for m in matches if 5 < len(m) < 200])

            # Relative
            matches = rel_path_pattern.findall(s)
            self.iocs['file_paths'].extend(matches)

        # Filter out Python internal paths
        self.iocs['file_paths'] = [
            p for p in set(self.iocs['file_paths'])
            if not any(x in p for x in ['site-packages', '__pycache__', 'Python3'])
        ]

        print(f"[+] Found {len(self.iocs['file_paths'])} unique file paths")

    def extract_registry_keys(self):
        """Extract Windows registry keys"""
        reg_pattern = re.compile(
            r'(?:HKEY_[A-Z_]+|HKLM|HKCU|HKCR|HKU|HKCC)\\[^\s]+'
        )

        for s in self.strings:
            matches = reg_pattern.findall(s)
            self.iocs['registry_keys'].extend(matches)

        self.iocs['registry_keys'] = list(set(self.iocs['registry_keys']))
        print(f"[+] Found {len(self.iocs['registry_keys'])} registry keys")

    def extract_telegram_handles(self):
        """Extract Telegram handles and channels"""
        telegram_pattern = re.compile(r'@[a-zA-Z0-9_]{5,}')

        for s in self.strings:
            matches = telegram_pattern.findall(s)
            self.iocs['telegram_handles'].extend(matches)

        self.iocs['telegram_handles'] = list(set(self.iocs['telegram_handles']))
        print(f"[+] Found {len(self.iocs['telegram_handles'])} Telegram handles")

    def extract_discord_webhooks(self):
        """Extract Discord webhook URLs"""
        webhook_pattern = re.compile(
            r'https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]+'
        )

        for s in self.strings:
            matches = webhook_pattern.findall(s)
            self.iocs['discord_webhooks'].extend(matches)

        self.iocs['discord_webhooks'] = list(set(self.iocs['discord_webhooks']))
        print(f"[+] Found {len(self.iocs['discord_webhooks'])} Discord webhooks")

    def extract_email_addresses(self):
        """Extract email addresses"""
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

        for s in self.strings:
            matches = email_pattern.findall(s)
            self.iocs['email_addresses'].extend(matches)

        self.iocs['email_addresses'] = list(set(self.iocs['email_addresses']))
        print(f"[+] Found {len(self.iocs['email_addresses'])} email addresses")

    def extract_crypto_addresses(self):
        """Extract cryptocurrency wallet addresses"""
        # Bitcoin
        btc_pattern = re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b')
        # Ethereum
        eth_pattern = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
        # Monero
        xmr_pattern = re.compile(r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b')

        for s in self.strings:
            btc_matches = btc_pattern.findall(s)
            eth_matches = eth_pattern.findall(s)
            xmr_matches = xmr_pattern.findall(s)

            self.iocs['cryptocurrency_addresses'].extend(btc_matches)
            self.iocs['cryptocurrency_addresses'].extend(eth_matches)
            self.iocs['cryptocurrency_addresses'].extend(xmr_matches)

        self.iocs['cryptocurrency_addresses'] = list(set(self.iocs['cryptocurrency_addresses']))
        print(f"[+] Found {len(self.iocs['cryptocurrency_addresses'])} crypto addresses")

    def extract_api_endpoints(self):
        """Extract API endpoints"""
        api_keywords = ['/api/', '/v1/', '/v2/', '/graphql', '/rest/']

        for s in self.strings:
            if any(kw in s.lower() for kw in api_keywords):
                if 'http' in s or s.startswith('/'):
                    self.iocs['api_endpoints'].append(s)

        self.iocs['api_endpoints'] = list(set(self.iocs['api_endpoints']))
        print(f"[+] Found {len(self.iocs['api_endpoints'])} API endpoints")

    def extract_suspicious_strings(self):
        """Extract strings indicating malicious behavior"""
        suspicious_keywords = {
            'credential_theft': ['password', 'token', 'api_key', 'secret', 'auth', 'credential'],
            'spam': ['spam', 'drop', 'mass', 'bulk', 'blast'],
            'evasion': ['bypass', 'evade', 'hide', 'stealth', 'antivirus', 'av'],
            'c2': ['command', 'control', 'beacon', 'callback', 'heartbeat'],
            'persistence': ['startup', 'registry', 'scheduled', 'autorun'],
            'data_theft': ['steal', 'grab', 'exfil', 'upload', 'send'],
            'automation': ['bot', 'automated', 'script', 'puppet'],
            'license': ['license', 'crack', 'keygen', 'activation', 'serial']
        }

        categorized = {}
        for category, keywords in suspicious_keywords.items():
            categorized[category] = []
            for s in self.strings:
                if isinstance(s, str) and 3 < len(s) < 500:
                    if any(kw in s.lower() for kw in keywords):
                        categorized[category].append(s)

        self.iocs['suspicious_strings'] = categorized
        total = sum(len(v) for v in categorized.values())
        print(f"[+] Found {total} suspicious strings across {len(categorized)} categories")

    def calculate_file_hashes(self):
        """Calculate hashes of malware files"""
        files_to_hash = [
            'XBot.exe',
            'XBot.pyc',
            'XBot.py'
        ]

        for filename in files_to_hash:
            filepath = self.analysis_dir.parent / filename
            if not filepath.exists():
                filepath = self.analysis_dir / filename

            if filepath.exists():
                self.iocs['file_hashes'][filename] = {
                    'md5': self._hash_file(filepath, 'md5'),
                    'sha1': self._hash_file(filepath, 'sha1'),
                    'sha256': self._hash_file(filepath, 'sha256')
                }
                print(f"[+] Calculated hashes for {filename}")

    def _hash_file(self, filepath: Path, algorithm: str) -> str:
        """Calculate hash of a file"""
        h = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def generate_sigma_rules(self) -> str:
        """Generate Sigma detection rules"""
        sigma = f"""title: XBot Twitter Spam Malware Detection
id: {hashlib.md5(b'xbot-malware').hexdigest()}
status: experimental
description: Detects XBot Twitter spam bot activity
author: Security Research
date: 2024/11/14
references:
    - Internal malware analysis
tags:
    - attack.execution
    - attack.persistence
    - attack.credential_access
logsource:
    category: process_creation
    product: windows
detection:
    selection_files:
        - Image|endswith: '\\XBot.exe'
        - CommandLine|contains: 'XBot'
    selection_paths:
        - TargetFilename|contains:
"""

        for path in self.iocs['file_paths'][:10]:
            sigma += f"            - '{path}'\n"

        sigma += """    condition: selection_files or selection_paths
falsepositives:
    - Unlikely
level: high
"""
        return sigma

    def generate_yara_rules(self) -> str:
        """Generate YARA detection rules"""
        yara = """rule XBot_Twitter_Spam_Malware
{
    meta:
        description = "Detects XBot Twitter spam bot malware"
        author = "Security Research"
        date = "2024-11-14"
        hash = "See analysis report"
        severity = "high"

    strings:
        // Unique identifiers
        $xbot1 = "XBot V2.1" ascii wide
        $xbot2 = "DolphinBot" ascii wide
        $xbot3 = ".xbot_profiles.json" ascii wide

        // Telegram reference
        $telegram = "@PurchaseTwitterXBot" ascii wide

        // Spam indicators
        $spam1 = "Hit my pinned post" ascii wide
        $spam2 = "Please add me to your groups" ascii wide
        $spam3 = "drop_message" ascii wide
        $spam4 = "drop_limit" ascii wide

        // License system
        $license1 = "license_key" ascii wide
        $license2 = "Enter License Key" ascii wide

        // API/Settings
        $api1 = "CLIENT_ID" ascii wide
        $api2 = "CLIENT_PASSWORD" ascii wide

        // Libraries
        $lib1 = "playwright" ascii
        $lib2 = "keyring" ascii

    condition:
        uint16(0) == 0x5A4D and  // PE header
        (
            2 of ($xbot*) or
            ($telegram and 2 of ($spam*)) or
            (3 of ($spam*) and 1 of ($license*)) or
            (all of ($lib*) and 1 of ($api*))
        )
}

rule XBot_PyInstaller_Bootloader
{
    meta:
        description = "Detects PyInstaller-packed XBot"
        author = "Security Research"

    strings:
        $pyi1 = "PyInstaller" ascii
        $pyi2 = "_MEIPASS" ascii
        $pyi3 = "PYZ-00.pyz" ascii
        $pyi4 = "pyiboot01_bootstrap" ascii

        $xbot = "XBot" ascii wide nocase

    condition:
        uint16(0) == 0x5A4D and
        2 of ($pyi*) and $xbot
}
"""
        return yara

    def run_extraction(self):
        """Run all IOC extraction"""
        print("[*] Starting IOC extraction...")

        self.load_strings()

        print("\n[*] Extracting network indicators...")
        self.extract_urls()
        self.extract_domains()
        self.extract_ips()
        self.extract_api_endpoints()

        print("\n[*] Extracting communication indicators...")
        self.extract_telegram_handles()
        self.extract_discord_webhooks()
        self.extract_email_addresses()

        print("\n[*] Extracting file system indicators...")
        self.extract_file_paths()
        self.extract_registry_keys()

        print("\n[*] Extracting financial indicators...")
        self.extract_crypto_addresses()

        print("\n[*] Extracting suspicious strings...")
        self.extract_suspicious_strings()

        print("\n[*] Calculating file hashes...")
        self.calculate_file_hashes()

        print("\n[*] Generating detection rules...")

    def save_results(self, output_dir: Path):
        """Save IOC results"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # Save JSON
        json_path = output_dir / 'xbot_iocs.json'
        with open(json_path, 'w') as f:
            json.dump(self.iocs, f, indent=2)
        print(f"[+] IOCs saved to {json_path}")

        # Save human-readable
        txt_path = output_dir / 'xbot_iocs.txt'
        with open(txt_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("XBot Malware - Indicators of Compromise\n")
            f.write("=" * 80 + "\n\n")

            if self.iocs['urls']:
                f.write("\n## URLS\n" + "-" * 80 + "\n")
                for url in self.iocs['urls']:
                    f.write(f"{url}\n")

            if self.iocs['domains']:
                f.write("\n## DOMAINS\n" + "-" * 80 + "\n")
                for domain in self.iocs['domains']:
                    f.write(f"{domain}\n")

            if self.iocs['telegram_handles']:
                f.write("\n## TELEGRAM HANDLES\n" + "-" * 80 + "\n")
                for handle in self.iocs['telegram_handles']:
                    f.write(f"{handle}\n")

            if self.iocs['file_paths']:
                f.write("\n## FILE PATHS\n" + "-" * 80 + "\n")
                for path in self.iocs['file_paths'][:50]:  # Top 50
                    f.write(f"{path}\n")

            if self.iocs['file_hashes']:
                f.write("\n## FILE HASHES\n" + "-" * 80 + "\n")
                for filename, hashes in self.iocs['file_hashes'].items():
                    f.write(f"\n{filename}:\n")
                    for alg, hash_val in hashes.items():
                        f.write(f"  {alg.upper()}: {hash_val}\n")

            f.write("\n## SUSPICIOUS STRINGS BY CATEGORY\n" + "-" * 80 + "\n")
            for category, strings in self.iocs['suspicious_strings'].items():
                if strings:
                    f.write(f"\n### {category.upper()}\n")
                    for s in strings[:20]:  # Top 20 per category
                        f.write(f"  - {s}\n")

        print(f"[+] Human-readable IOCs saved to {txt_path}")

        # Save YARA rules
        yara_path = output_dir / 'xbot_detection.yar'
        with open(yara_path, 'w') as f:
            f.write(self.generate_yara_rules())
        print(f"[+] YARA rules saved to {yara_path}")

        # Save Sigma rules
        sigma_path = output_dir / 'xbot_detection.yml'
        with open(sigma_path, 'w') as f:
            f.write(self.generate_sigma_rules())
        print(f"[+] Sigma rules saved to {sigma_path}")

        print("\n[+] IOC extraction complete!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_iocs.py <XBot_strings.txt> [output_dir]")
        print("\nExample:")
        print("  python3 extract_iocs.py XBot_strings.txt ./iocs")
        sys.exit(1)

    strings_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './xbot_iocs'

    extractor = IOCExtractor(strings_file)
    extractor.run_extraction()
    extractor.save_results(output_dir)


if __name__ == '__main__':
    main()
