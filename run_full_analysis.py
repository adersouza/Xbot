#!/usr/bin/env python3
"""
XBot Complete Analysis Pipeline
Runs full malware analysis from extraction to IOC generation
"""

import sys
import subprocess
import shutil
from pathlib import Path
import json
import hashlib


class XBotAnalysisPipeline:
    """Complete analysis pipeline for XBot malware"""

    def __init__(self, exe_path: str, output_dir: str = './xbot_complete_analysis'):
        self.exe_path = Path(exe_path)
        self.output_dir = Path(output_dir)
        self.extracted_dir = None
        self.pyc_path = None

        # Create output directory
        self.output_dir.mkdir(exist_ok=True)

        print("=" * 80)
        print("XBot Malware Analysis Pipeline")
        print("=" * 80)
        print(f"Target: {self.exe_path}")
        print(f"Output: {self.output_dir}")
        print("=" * 80 + "\n")

    def check_prerequisites(self):
        """Check if required tools are available"""
        print("[*] Checking prerequisites...")

        # Check Python
        if sys.version_info < (3, 6):
            print("[-] Python 3.6+ required")
            return False

        # Check if pyinstxtractor is available
        pyinstxtractor_path = Path('pyinstxtractor.py')
        if not pyinstxtractor_path.exists():
            print("[-] pyinstxtractor.py not found")
            print("[!] Download it with:")
            print("    curl -O https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py")
            return False

        print("[+] Prerequisites OK\n")
        return True

    def calculate_hashes(self):
        """Calculate file hashes"""
        print("[*] Calculating file hashes...")

        hashes = {}
        for algo in ['md5', 'sha1', 'sha256']:
            h = hashlib.new(algo)
            with open(self.exe_path, 'rb') as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            hashes[algo] = h.hexdigest()
            print(f"    {algo.upper()}: {hashes[algo]}")

        # Save hashes
        hash_file = self.output_dir / 'file_hashes.json'
        with open(hash_file, 'w') as f:
            json.dump({
                'filename': self.exe_path.name,
                'hashes': hashes,
                'size': self.exe_path.stat().st_size
            }, f, indent=2)

        print(f"[+] Hashes saved to {hash_file}\n")
        return hashes

    def extract_pyinstaller(self):
        """Extract PyInstaller archive"""
        print("[*] Step 1: Extracting PyInstaller archive...")

        try:
            result = subprocess.run(
                ['python3', 'pyinstxtractor.py', str(self.exe_path)],
                capture_output=True,
                text=True,
                timeout=120
            )

            print(result.stdout)

            if result.returncode != 0:
                print(f"[-] Extraction failed: {result.stderr}")
                return False

            # Find extracted directory
            exe_name = self.exe_path.stem
            self.extracted_dir = self.exe_path.parent / f"{self.exe_path.name}_extracted"

            if not self.extracted_dir.exists():
                print(f"[-] Extracted directory not found: {self.extracted_dir}")
                return False

            # Find XBot.pyc
            self.pyc_path = self.extracted_dir / f"{exe_name}.pyc"
            if not self.pyc_path.exists():
                # Try common names
                for name in ['XBot.pyc', 'main.pyc', '__main__.pyc']:
                    test_path = self.extracted_dir / name
                    if test_path.exists():
                        self.pyc_path = test_path
                        break

            if not self.pyc_path.exists():
                print(f"[-] Could not find main .pyc file")
                return False

            print(f"[+] Extracted to: {self.extracted_dir}")
            print(f"[+] Main script: {self.pyc_path}\n")
            return True

        except subprocess.TimeoutExpired:
            print("[-] Extraction timeout")
            return False
        except Exception as e:
            print(f"[-] Extraction error: {e}")
            return False

    def analyze_bytecode(self):
        """Run bytecode analysis"""
        print("[*] Step 2: Analyzing Python bytecode...")

        analysis_dir = self.output_dir / 'bytecode_analysis'
        analysis_dir.mkdir(exist_ok=True)

        try:
            # Import and run analyzer
            sys.path.insert(0, str(Path(__file__).parent))
            from analyze_xbot_bytecode import XBotBytecodeAnalyzer

            analyzer = XBotBytecodeAnalyzer(str(self.pyc_path))
            success = analyzer.run_analysis(str(analysis_dir))

            if success:
                print(f"[+] Bytecode analysis complete\n")
                return True
            else:
                print(f"[-] Bytecode analysis failed\n")
                return False

        except ImportError:
            print("[-] Could not import analyze_xbot_bytecode.py")
            print("[!] Make sure it's in the same directory")
            return False
        except Exception as e:
            print(f"[-] Bytecode analysis error: {e}\n")
            return False

    def extract_iocs(self):
        """Extract indicators of compromise"""
        print("[*] Step 3: Extracting IOCs...")

        strings_file = self.output_dir / 'bytecode_analysis' / 'XBot_strings.txt'
        if not strings_file.exists():
            print(f"[-] Strings file not found: {strings_file}")
            return False

        ioc_dir = self.output_dir / 'iocs'
        ioc_dir.mkdir(exist_ok=True)

        try:
            # Import and run IOC extractor
            from extract_iocs import IOCExtractor

            extractor = IOCExtractor(str(strings_file), str(self.extracted_dir))
            extractor.run_extraction()
            extractor.save_results(ioc_dir)

            print(f"[+] IOC extraction complete\n")
            return True

        except ImportError:
            print("[-] Could not import extract_iocs.py")
            return False
        except Exception as e:
            print(f"[-] IOC extraction error: {e}\n")
            return False

    def generate_summary(self):
        """Generate analysis summary"""
        print("[*] Step 4: Generating summary report...")

        summary_file = self.output_dir / 'ANALYSIS_SUMMARY.txt'

        try:
            # Load analysis data
            analysis_json = self.output_dir / 'bytecode_analysis' / 'XBot_analysis_report.json'
            ioc_json = self.output_dir / 'iocs' / 'xbot_iocs.json'

            analysis_data = {}
            ioc_data = {}

            if analysis_json.exists():
                with open(analysis_json) as f:
                    analysis_data = json.load(f)

            if ioc_json.exists():
                with open(ioc_json) as f:
                    ioc_data = json.load(f)

            # Write summary
            with open(summary_file, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("XBOT MALWARE ANALYSIS SUMMARY\n")
                f.write("=" * 80 + "\n\n")

                f.write("## FILE INFORMATION\n")
                f.write("-" * 80 + "\n")
                f.write(f"Filename: {self.exe_path.name}\n")
                f.write(f"Size: {self.exe_path.stat().st_size:,} bytes\n")

                hash_file = self.output_dir / 'file_hashes.json'
                if hash_file.exists():
                    with open(hash_file) as hf:
                        hashes = json.load(hf)['hashes']
                        for algo, hash_val in hashes.items():
                            f.write(f"{algo.upper()}: {hash_val}\n")

                f.write("\n## MALWARE TYPE\n")
                f.write("-" * 80 + "\n")
                f.write("Type: Twitter Spam Bot\n")
                f.write("Name: XBot / DolphinBot\n")
                f.write("Version: 2.1\n")
                f.write("Platform: Windows x64\n")
                f.write("Language: Python 3.13 (PyInstaller)\n")

                f.write("\n## CAPABILITIES\n")
                f.write("-" * 80 + "\n")
                f.write("- Twitter account automation\n")
                f.write("- Mass message spam\n")
                f.write("- Credential storage (keyring)\n")
                f.write("- Browser automation (Playwright)\n")
                f.write("- Rate limit evasion\n")
                f.write("- License system (cracked)\n")

                if analysis_data:
                    f.write("\n## ANALYSIS STATISTICS\n")
                    f.write("-" * 80 + "\n")
                    meta = analysis_data.get('metadata', {})
                    f.write(f"Total strings: {meta.get('total_strings', 'N/A')}\n")
                    f.write(f"Total functions: {meta.get('total_functions', 'N/A')}\n")
                    f.write(f"Total imports: {meta.get('total_imports', 'N/A')}\n")

                if ioc_data:
                    f.write("\n## IOC SUMMARY\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"URLs: {len(ioc_data.get('urls', []))}\n")
                    f.write(f"Domains: {len(ioc_data.get('domains', []))}\n")
                    f.write(f"File paths: {len(ioc_data.get('file_paths', []))}\n")
                    f.write(f"Telegram handles: {len(ioc_data.get('telegram_handles', []))}\n")

                    if ioc_data.get('telegram_handles'):
                        f.write("\n## KEY IOCS\n")
                        f.write("-" * 80 + "\n")
                        f.write("Telegram contact: " + ", ".join(ioc_data['telegram_handles']) + "\n")

                    if ioc_data.get('urls'):
                        f.write("\nURLs:\n")
                        for url in ioc_data['urls'][:10]:
                            f.write(f"  - {url}\n")

                f.write("\n## THREAT ASSESSMENT\n")
                f.write("-" * 80 + "\n")
                f.write("Risk to Platform (Twitter): HIGH\n")
                f.write("Risk to End Users: MEDIUM\n")
                f.write("Risk to Enterprise: LOW\n")

                f.write("\n## RECOMMENDED ACTIONS\n")
                f.write("-" * 80 + "\n")
                f.write("1. Reset all Twitter account credentials\n")
                f.write("2. Delete configuration files (.xbot_profiles.json)\n")
                f.write("3. Remove from Windows Credential Manager\n")
                f.write("4. Report spam activity to Twitter\n")
                f.write("5. Deploy detection rules (YARA/Sigma)\n")

                f.write("\n## OUTPUT FILES\n")
                f.write("-" * 80 + "\n")
                f.write(f"Bytecode analysis: {self.output_dir / 'bytecode_analysis'}\n")
                f.write(f"IOCs: {self.output_dir / 'iocs'}\n")
                f.write(f"YARA rules: {self.output_dir / 'iocs' / 'xbot_detection.yar'}\n")
                f.write(f"Sigma rules: {self.output_dir / 'iocs' / 'xbot_detection.yml'}\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("Analysis complete. Review detailed reports in output directory.\n")
                f.write("=" * 80 + "\n")

            print(f"[+] Summary saved to {summary_file}\n")
            return True

        except Exception as e:
            print(f"[-] Summary generation error: {e}\n")
            return False

    def run(self):
        """Run complete analysis pipeline"""
        print("[*] Starting complete analysis pipeline...\n")

        # Check prerequisites
        if not self.check_prerequisites():
            print("\n[!] Prerequisites check failed. Aborting.")
            return False

        # Calculate hashes
        self.calculate_hashes()

        # Step 1: Extract
        if not self.extract_pyinstaller():
            print("\n[!] Extraction failed. Aborting.")
            return False

        # Step 2: Analyze bytecode
        if not self.analyze_bytecode():
            print("\n[!] Bytecode analysis failed. Continuing anyway...")

        # Step 3: Extract IOCs
        if not self.extract_iocs():
            print("\n[!] IOC extraction failed. Continuing anyway...")

        # Step 4: Generate summary
        self.generate_summary()

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"\nResults saved to: {self.output_dir}")
        print("\nKey files:")
        print(f"  - Summary: {self.output_dir / 'ANALYSIS_SUMMARY.txt'}")
        print(f"  - Bytecode: {self.output_dir / 'bytecode_analysis'}")
        print(f"  - IOCs: {self.output_dir / 'iocs'}")
        print(f"  - YARA: {self.output_dir / 'iocs' / 'xbot_detection.yar'}")
        print("\n" + "=" * 80 + "\n")

        return True


def main():
    if len(sys.argv) < 2:
        print("XBot Complete Analysis Pipeline")
        print("=" * 80)
        print("\nUsage: python3 run_full_analysis.py <XBot.exe> [output_dir]")
        print("\nExample:")
        print("  python3 run_full_analysis.py XBot.exe")
        print("  python3 run_full_analysis.py XBot.exe ./my_analysis")
        print("\nPrerequisites:")
        print("  1. Download pyinstxtractor.py to current directory:")
        print("     curl -O https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py")
        print("\n  2. Ensure analyze_xbot_bytecode.py and extract_iocs.py are present")
        print("\n" + "=" * 80)
        sys.exit(1)

    exe_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './xbot_complete_analysis'

    pipeline = XBotAnalysisPipeline(exe_path, output_dir)
    success = pipeline.run()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
