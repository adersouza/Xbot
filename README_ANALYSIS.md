# XBot Malware Analysis Toolkit

Complete analysis toolkit for reverse engineering and documenting the XBot Twitter spam malware.

## Overview

This repository contains:
- **Decompiled bootloader** (from Ghidra)
- **Extracted Python bytecode** (from pyinstxtractor)
- **Analysis scripts** (Python tools for bytecode analysis)
- **IOC extractors** (Generate indicators of compromise)
- **Detection rules** (YARA and Sigma signatures)
- **Complete documentation** (Technical analysis and findings)

## Table of Contents

1. [Quick Start](#quick-start)
2. [Analysis Scripts](#analysis-scripts)
3. [Step-by-Step Analysis](#step-by-step-analysis)
4. [File Structure](#file-structure)
5. [Requirements](#requirements)

---

## Quick Start

### Prerequisites

```bash
# macOS
brew install python3

# Install Python packages
pip3 install --user pyinstxtractor

# Or download pyinstxtractor manually
curl -O https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py
```

### One-Command Analysis

```bash
# Run complete analysis pipeline
python3 run_full_analysis.py XBot.exe
```

This will:
1. Extract PyInstaller archive
2. Analyze bytecode
3. Extract IOCs
4. Generate detection rules
5. Create comprehensive report

---

## Analysis Scripts

### 1. analyze_xbot_bytecode.py

**Purpose:** Analyze Python 3.13 bytecode without decompiling

**Usage:**
```bash
python3 analyze_xbot_bytecode.py <XBot.pyc> [output_dir]

# Example
python3 analyze_xbot_bytecode.py "XBot.exe_extracted/XBot.pyc" ./analysis_output
```

**Outputs:**
- `XBot_disassembly.txt` - Complete bytecode disassembly
- `XBot_analysis_report.json` - Machine-readable report
- `XBot_analysis_report.txt` - Human-readable report
- `XBot_strings.txt` - All extracted strings

**Features:**
- Recursively extracts all strings
- Identifies function definitions
- Finds imports and API calls
- Locates URLs, credentials, file paths
- Categorizes suspicious strings

---

### 2. extract_iocs.py

**Purpose:** Extract indicators of compromise for threat intelligence

**Usage:**
```bash
python3 extract_iocs.py <XBot_strings.txt> [output_dir]

# Example
python3 extract_iocs.py analysis_output/XBot_strings.txt ./iocs
```

**Outputs:**
- `xbot_iocs.json` - Structured IOC data
- `xbot_iocs.txt` - Human-readable IOCs
- `xbot_detection.yar` - YARA detection rules
- `xbot_detection.yml` - Sigma detection rules

**Extracted IOCs:**
- URLs and domains
- IP addresses
- File paths
- Registry keys
- Telegram handles
- Discord webhooks
- Email addresses
- Cryptocurrency addresses
- API endpoints
- File hashes (MD5, SHA1, SHA256)

---

### 3. run_full_analysis.py

**Purpose:** Master script that runs complete analysis pipeline

**Usage:**
```bash
python3 run_full_analysis.py <XBot.exe> [output_dir]

# Example
python3 run_full_analysis.py XBot.exe ./complete_analysis
```

**Pipeline:**
1. Extract PyInstaller archive with pyinstxtractor
2. Run bytecode analysis
3. Extract IOCs
4. Generate detection rules
5. Calculate file hashes
6. Create summary report

---

## Step-by-Step Analysis

### Phase 1: Extraction

Extract the PyInstaller bundle:

```bash
# Download extraction tool
curl -O https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py

# Extract
python3 pyinstxtractor.py XBot.exe

# Navigate to extracted files
cd "XBot.exe_extracted"
ls -lh
```

**Expected files:**
- `XBot.pyc` (200KB) - Main malware logic
- `PYZ.pyz` (12MB) - Compressed Python modules
- `python313.dll` - Python runtime
- Various `.pyd` files - Extension modules
- `background.jpg` - GUI background
- `assets/` - Icons and resources

---

### Phase 2: Bytecode Analysis

Analyze the compiled Python bytecode:

```bash
# Run bytecode analyzer
python3 ../analyze_xbot_bytecode.py XBot.pyc ../analysis

# View results
cat ../analysis/XBot_analysis_report.txt
```

**What to look for:**
- Function names and purposes
- Imported modules (playwright, keyring, etc.)
- Strings revealing functionality
- API endpoints and URLs
- Credential-related code

---

### Phase 3: IOC Extraction

Extract indicators for detection:

```bash
# Extract IOCs
python3 ../extract_iocs.py ../analysis/XBot_strings.txt ../iocs

# View IOCs
cat ../iocs/xbot_iocs.txt
```

**Key IOCs:**
- `@PurchaseTwitterXBot` - Telegram handle
- `XBot V2.1` - Version string
- `.xbot_profiles.json` - Configuration file
- Specific URLs and domains

---

### Phase 4: Detection Rules

Use generated YARA/Sigma rules:

```bash
# Test YARA rule
yara ../iocs/xbot_detection.yar XBot.exe

# Review Sigma rule
cat ../iocs/xbot_detection.yml
```

---

## File Structure

```
Xbot/
├── XBot.exe                          # Original malware sample
├── c                                 # Ghidra decompiled bootloader
│
├── Analysis Scripts:
│   ├── analyze_xbot_bytecode.py      # Bytecode analyzer
│   ├── extract_iocs.py               # IOC extractor
│   └── run_full_analysis.py          # Master pipeline
│
├── Documentation:
│   ├── XBOT_MALWARE_ANALYSIS.md      # Complete technical analysis
│   ├── REVERSE_ENGINEERING_ANALYSIS.md  # Bootloader analysis
│   ├── EXTRACTION_GUIDE.md           # PyInstaller extraction guide
│   ├── KEY_FINDINGS.md               # Summary of findings
│   └── README_ANALYSIS.md            # This file
│
└── Generated Outputs (after analysis):
    ├── analysis/
    │   ├── XBot_disassembly.txt
    │   ├── XBot_analysis_report.json
    │   ├── XBot_analysis_report.txt
    │   └── XBot_strings.txt
    │
    └── iocs/
        ├── xbot_iocs.json
        ├── xbot_iocs.txt
        ├── xbot_detection.yar
        └── xbot_detection.yml
```

---

## Requirements

### Python Packages

```bash
# Core (built-in)
- dis
- marshal
- struct
- hashlib
- json
- re
- pathlib

# External (optional)
- pyinstxtractor  # For initial extraction
```

### System Tools

```bash
# macOS
- python3 (comes with OS)
- strings (comes with OS)
- curl (comes with OS)

# Optional
- yara (for testing YARA rules)
- jq (for parsing JSON reports)
```

---

## Usage Examples

### Example 1: Quick Analysis

```bash
# Extract and analyze in one go
python3 run_full_analysis.py XBot.exe ./output
```

### Example 2: Manual Deep Dive

```bash
# Step 1: Extract
python3 pyinstxtractor.py XBot.exe

# Step 2: Analyze bytecode
python3 analyze_xbot_bytecode.py \
  "XBot.exe_extracted/XBot.pyc" \
  ./bytecode_analysis

# Step 3: Extract IOCs
python3 extract_iocs.py \
  bytecode_analysis/XBot_strings.txt \
  ./threat_intel

# Step 4: Review results
cat bytecode_analysis/XBot_analysis_report.txt
cat threat_intel/xbot_iocs.txt
```

### Example 3: Searching Specific Patterns

```bash
# Find all credential-related strings
grep -i "password\|token\|secret\|auth" analysis/XBot_strings.txt

# Find all URLs
grep -E "https?://" analysis/XBot_strings.txt

# Find Telegram references
grep -i "telegram" analysis/XBot_strings.txt
```

### Example 4: Testing Detection Rules

```bash
# Test YARA rule
yara iocs/xbot_detection.yar XBot.exe

# Test on directory
yara -r iocs/xbot_detection.yar /path/to/samples/

# Verbose output
yara -s iocs/xbot_detection.yar XBot.exe
```

---

## Understanding the Output

### Bytecode Analysis Report

**XBot_analysis_report.txt** contains:

```
## METADATA
- Total strings found
- Total functions identified
- Imports detected

## URLS FOUND
- Network endpoints
- API URLs
- External resources

## CREDENTIAL-RELATED STRINGS
- Password fields
- Token references
- API keys

## SUSPICIOUS STRINGS
- Spam-related terms
- Evasion keywords
- License bypasses
```

### IOC Report

**xbot_iocs.txt** contains:

```
## URLS
- All HTTP/HTTPS endpoints

## DOMAINS
- Domain names extracted

## TELEGRAM HANDLES
- @PurchaseTwitterXBot (seller)

## FILE PATHS
- Configuration files
- Temp directories
- Installation paths

## FILE HASHES
- MD5, SHA1, SHA256 of malware files
```

---

## Detection Integration

### Import to SIEM

```bash
# Convert JSON IOCs to CSV for SIEM import
jq -r '.urls[]' iocs/xbot_iocs.json > urls.csv
jq -r '.domains[]' iocs/xbot_iocs.json > domains.csv
```

### Threat Intelligence Platform

```bash
# Upload IOC JSON to TIP
curl -X POST https://tip.example.com/api/iocs \
  -H "Content-Type: application/json" \
  -d @iocs/xbot_iocs.json
```

### Network Monitoring

```bash
# Create blocklist from domains
jq -r '.domains[]' iocs/xbot_iocs.json > blocklist.txt

# Use in firewall/proxy
# (Implementation depends on your security stack)
```

---

## Advanced Analysis

### Bytecode Disassembly Deep Dive

The `XBot_disassembly.txt` file contains Python bytecode instructions:

```python
# Example disassembly snippet
  0 LOAD_CONST               0 ('XBot V2.1')
  2 STORE_NAME               1 (version)
  4 LOAD_NAME                2 (keyring)
  6 LOAD_METHOD              3 (get_password)
  8 LOAD_CONST               1 ('XBot')
 10 LOAD_CONST               2 ('client_id')
 12 CALL_METHOD              2
```

**How to read:**
- Each line is a bytecode instruction
- Numbers are instruction offsets
- LOAD_CONST loads constants
- STORE_NAME stores to variables
- CALL_METHOD calls functions

### Finding Specific Functionality

```bash
# Find crypto payment code
grep -A 10 -B 10 "crypto" analysis/XBot_disassembly.txt

# Find license validation
grep -A 20 "license" analysis/XBot_disassembly.txt

# Find Twitter automation
grep -A 15 "playwright\|browser" analysis/XBot_disassembly.txt
```

---

## Troubleshooting

### Issue: "Python version not supported"

**Problem:** XBot uses Python 3.13, which is very new

**Solution:** The analysis scripts don't need to decompile, they analyze bytecode directly. This works regardless of Python version.

### Issue: "Permission denied"

**Problem:** Can't execute scripts

**Solution:**
```bash
chmod +x analyze_xbot_bytecode.py
chmod +x extract_iocs.py
chmod +x run_full_analysis.py
```

### Issue: "Module not found"

**Problem:** Missing dependencies

**Solution:**
```bash
# Check Python version
python3 --version

# Install to user directory
pip3 install --user <package>

# Or use system Python
sudo pip3 install <package>
```

### Issue: "File not found"

**Problem:** Incorrect path to XBot.pyc

**Solution:**
```bash
# Find the file
find . -name "XBot.pyc"

# Use absolute path
python3 analyze_xbot_bytecode.py "/full/path/to/XBot.pyc" ./output
```

---

## Safety Precautions

⚠️ **WARNING: This is active malware. Follow safety protocols:**

1. **Isolated Environment**
   - Use a VM or sandbox
   - No network access during analysis
   - Take snapshots before running scripts

2. **Do NOT Execute XBot.exe**
   - Analysis scripts are safe
   - Never run the actual malware
   - Only analyze extracted files

3. **Credential Protection**
   - If `.xbot_profiles.json` exists, it contains credentials
   - Reset any passwords found
   - Report compromised accounts

4. **Legal Compliance**
   - Ensure authorization for analysis
   - Follow responsible disclosure
   - Comply with local laws

---

## Contributing

To improve this analysis:

1. **Add More IOC Patterns**
   - Edit `extract_iocs.py`
   - Add regex patterns
   - Submit pull request

2. **Enhance Detection Rules**
   - Improve YARA signatures
   - Add Sigma rule variants
   - Test against samples

3. **Document New Findings**
   - Update `XBOT_MALWARE_ANALYSIS.md`
   - Add screenshots/examples
   - Explain new techniques

---

## Resources

### Tools

- **pyinstxtractor:** https://github.com/extremecoders-re/pyinstxtractor
- **Ghidra:** https://ghidra-sre.org/
- **YARA:** https://virustotal.github.io/yara/
- **Sigma:** https://github.com/SigmaHQ/sigma

### Documentation

- **Python Bytecode:** https://docs.python.org/3/library/dis.html
- **PyInstaller Format:** https://pyinstaller.org/en/stable/advanced-topics.html
- **Playwright:** https://playwright.dev/

### Threat Intel

- **VirusTotal:** Upload hashes for community intel
- **Hybrid Analysis:** Sandbox analysis
- **Any.run:** Interactive malware analysis

---

## License

This analysis toolkit is provided for **educational and security research purposes only**.

**Do NOT:**
- Use to enable malicious activity
- Distribute the malware samples
- Bypass platform protections

**Do:**
- Improve detection capabilities
- Educate security teams
- Contribute to threat intelligence

---

## Contact

For questions or collaboration:
- Open a GitHub issue
- Submit findings via pull request
- Contact: [Your organization's security team]

---

**Last Updated:** 2024-11-14
**Toolkit Version:** 1.0
**Malware Sample:** XBot v2.1
