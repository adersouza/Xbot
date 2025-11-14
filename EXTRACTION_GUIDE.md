# Python Payload Extraction Guide

This guide explains how to extract the embedded Python code from the PyInstaller executable for further analysis.

## Prerequisites

```bash
# Install required tools
pip install pyinstxtractor
pip install uncompyle6
# or
pip install decompyle3
```

## Method 1: Automated Extraction with pyinstxtractor

### Step 1: Extract the Archive

```bash
python pyinstxtractor.py XBot.exe
```

This creates a directory `XBot.exe_extracted/` containing:
- `PYZ-00.pyz` - Compressed Python library archive
- `*.pyd` / `*.dll` - Python extension modules
- `struct`, `pyimod*` - PyInstaller runtime modules
- Main script file (varies by name)

### Step 2: Identify the Main Script

```bash
cd XBot.exe_extracted/
ls -lh

# Look for the largest .pyc file or one matching the executable name
# Common names: XBot.pyc, __main__.pyc, main.pyc
```

### Step 3: Extract PYZ Archive (Optional)

If you need to extract all Python modules:

```bash
python -c "
import sys
sys.path.insert(0, '.')
from pyinstxtractor import PyInstArchive

archive = PyInstArchive('PYZ-00.pyz')
archive.open()
archive.extractFiles()
"
```

### Step 4: Decompile Python Bytecode

```bash
# For Python 3.8+
uncompyle6 XBot.pyc > XBot.py

# Or for newer Python versions
decompyle3 XBot.pyc > XBot.py

# Batch decompile all .pyc files
for file in *.pyc; do
    uncompyle6 "$file" > "${file%.pyc}.py"
done
```

## Method 2: Manual Extraction

### Understanding PyInstaller Archive Format

```
[PE Executable]
[Bootloader Code]
[Overlay Data]
  ├─ Cookie (24 bytes) - "MEI\014\013\012\013\016" + magic
  ├─ TOC Position (8 bytes)
  ├─ TOC Length (8 bytes)
  ├─ Python Version (4 bytes)
  └─ Archive Data (zlib compressed)
```

### Python Script for Manual Extraction

```python
#!/usr/bin/env python3
import struct
import zlib
import marshal

def extract_pyinstaller(exe_path):
    with open(exe_path, 'rb') as f:
        # Seek to end and find cookie
        f.seek(-24, 2)  # 24 bytes from end
        cookie = f.read(8)

        if cookie != b'MEI\x0c\x0b\x0a\x0b\x0e':
            print("Not a PyInstaller archive!")
            return

        # Read metadata
        magic = struct.unpack('!Q', f.read(8))[0]
        toc_pos = struct.unpack('!Q', f.read(8))[0]

        # Read TOC
        f.seek(toc_pos)
        toc_data = f.read()

        # Decompress if needed
        try:
            toc_data = zlib.decompress(toc_data)
        except:
            pass

        # Parse TOC entries
        pos = 0
        while pos < len(toc_data):
            entry_len = struct.unpack('!I', toc_data[pos:pos+4])[0]
            pos += 4

            entry = toc_data[pos:pos+entry_len]
            pos += entry_len

            # Extract entry data
            # Format: [entry_size][position][compressed_size][uncompressed_size][flag][type][name]
            # TODO: Parse and extract each entry

    print("Extraction complete!")

# Usage
extract_pyinstaller('XBot.exe')
```

## Method 3: Runtime Memory Extraction

### Using a Debugger

```bash
# Attach debugger (x64dbg, WinDbg, or OllyDbg)

# Set breakpoints at:
# 1. PyImport_ExecCodeModule - Captures bytecode before execution
# 2. PyRun_SimpleStringFlags - Captures string-based code
# 3. CreateFileW - Monitors file extraction to _MEI temp folder

# Run the executable and dump memory when breakpoint hits
```

### Using Process Monitor

```bash
# 1. Start Process Monitor (procmon.exe)
# 2. Filter: Process Name is XBot.exe
# 3. Filter: Operation is CreateFile or WriteFile
# 4. Run XBot.exe
# 5. Look for _MEI* directories in %TEMP%
# 6. Copy extracted files before process terminates
```

## Method 4: Using Python Archive Tools

```python
#!/usr/bin/env python3
from zipfile import ZipFile
import py_compile
import marshal

# Some PyInstaller builds use ZIP format
try:
    with ZipFile('XBot.exe', 'r') as zip_ref:
        zip_ref.extractall('extracted/')
        print("Extracted as ZIP")
except:
    print("Not a ZIP archive, use pyinstxtractor")
```

## Post-Extraction Analysis

### 1. Examine Main Script

```bash
# View decompiled source
cat XBot.py

# Look for:
# - Network connections (socket, requests, urllib)
# - File operations (open, read, write)
# - Process execution (subprocess, os.system)
# - Encryption/obfuscation
# - C2 server addresses
# - Exfiltration mechanisms
```

### 2. Analyze Dependencies

```bash
# Check imported modules
grep -E "^import |^from " XBot.py

# Common malware imports:
# - socket, requests - Network operations
# - subprocess, os - Command execution
# - ctypes - Windows API access
# - cryptography, pycryptodome - Encryption
# - keyring, win32crypt - Credential theft
# - pyautogui, PIL - Screenshots
# - pyperclip - Clipboard access
```

### 3. Search for IOCs

```bash
# Extract URLs/IPs
grep -oE 'https?://[^"'\'']+' XBot.py
grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' XBot.py

# Extract file paths
grep -oE '[A-Z]:\\[^"'\'']+' XBot.py

# Extract registry keys
grep -i 'HKEY_' XBot.py
```

### 4. Deobfuscation

If the code is obfuscated:

```python
# Common obfuscation techniques:
# 1. Base64 encoding
import base64
base64.b64decode('encoded_string')

# 2. ROT13 or Caesar cipher
import codecs
codecs.decode('string', 'rot_13')

# 3. Hex encoding
bytes.fromhex('hexstring')

# 4. Exec/eval obfuscation
# Replace exec() with print() to see what would be executed
```

## Safety Precautions

1. **Isolated Environment**: Perform all analysis in a VM or sandbox
2. **Network Isolation**: Disconnect network before running executable
3. **Snapshots**: Take VM snapshots before each step
4. **Monitoring**: Use Process Monitor, Wireshark, and other tools
5. **Documentation**: Record all findings and IOCs

## Common File Locations After Extraction

```
%TEMP%\_MEI<random>\     - Runtime extraction directory
XBot.exe_extracted\       - pyinstxtractor output
XBot.exe_extracted\PYZ-00.pyz - Python library archive
XBot.exe_extracted\XBot.pyc   - Main script (compiled)
XBot.exe_extracted\base_library.zip - Standard library (if present)
```

## Troubleshooting

### Issue: "Not a valid PyInstaller archive"

**Solution**: The executable may be:
- Packed with a different tool (py2exe, cx_Freeze)
- Encrypted or obfuscated
- Corrupted during download/transfer

### Issue: Decompilation fails

**Solution**:
- Try different decompilers (uncompyle6, decompyle3, pycdc)
- Check Python version compatibility
- May be using newer Python features not supported by decompiler

### Issue: Empty or missing files

**Solution**:
- Check if executable is a "onefile" build
- Files may be in memory only
- Try runtime extraction method

## References

- [PyInstaller Documentation](https://pyinstaller.org/)
- [pyinstxtractor GitHub](https://github.com/extremecoders-re/pyinstxtractor)
- [uncompyle6 GitHub](https://github.com/rocky/python-uncompyle6/)
- [Analyzing Python Malware](https://github.com/countercept/python-exe-unpacker)

---

**Note**: Always ensure you have proper authorization before analyzing executables. This guide is for educational and authorized security research purposes only.
