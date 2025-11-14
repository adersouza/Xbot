# XBot.exe - Key Findings Summary

## Quick Reference

**File Type**: PyInstaller-packaged Python executable
**Platform**: Windows x64
**Risk Level**: HIGH - Likely malware
**Analysis Date**: 2025-11-14

## Critical Findings

### 1. Executable Type: PyInstaller Bundle

The decompiled code reveals this is NOT a native C/C++ application, but rather a **PyInstaller bootloader** that extracts and runs embedded Python code.

**Key Evidence**:
- PyInstaller environment variables (`PYINSTALLER_RESET_ENVIRONMENT`, `_MEIPASS`)
- PYZ archive format references
- Python C API function imports (`Py_Initialize`, `PyImport_ExecCodeModule`)
- Hidden window class: `PyInstallerOnefileHiddenWindow`

### 2. Embedded Archive Structure

```
XBot.exe
├─ Bootloader (Native Windows code)
├─ Python Interpreter (Embedded)
└─ PYZ Archive (Compressed Python modules)
   ├─ Main Script (The actual malware)
   ├─ Python Libraries
   └─ Dependencies
```

### 3. Suspicious Capabilities

#### Network Operations
- Socket error messages indicate networking functionality
- Connection handling: "connection refused", "connection reset", "not connected"
- **Implication**: C2 (Command & Control) communication likely

#### Process Manipulation
- `CreateProcessW` - Can spawn child processes
- `OpenProcessToken` - Can access process security tokens
- `GetTokenInformation` - Can query privilege levels
- **Implication**: May attempt privilege escalation or process injection

#### Hidden Execution
- Creates hidden window for message handling
- GUI error dialogs mask as legitimate application
- **Implication**: Designed to run stealthily

#### File System Operations
- Extracts files to temporary directory (`%TEMP%\_MEI<random>`)
- Archive extraction with zlib compression
- **Implication**: May drop additional payloads

## Function Reference (Key Addresses)

### Bootloader Entry Points

| Address       | Function                  | Purpose                          |
|---------------|---------------------------|----------------------------------|
| 0x140001000   | Entry/Main Function       | Program initialization           |
| 0x140001050   | Archive Extraction        | Extracts files from PYZ archive  |
| 0x140001210   | Decompression Handler     | zlib inflate operations          |
| 0x140002fe0   | Python Script Executor    | Runs __main__ module             |
| 0x1400037c0   | Main Execution Flow       | Orchestrates bootloader stages   |

### Python API Imports (around 0x140005830)

```c
Py_InitializeFromConfig   // Initialize Python runtime
Py_Finalize              // Cleanup Python runtime
PyImport_AddModule       // Load Python module
PyImport_ExecCodeModule  // Execute compiled bytecode
PyImport_ImportModule    // Import module by name
PyRun_SimpleStringFlags  // Run Python code string
```

### Windows API Calls

| Function                  | DLL          | Risk    | Purpose                      |
|---------------------------|--------------|---------|------------------------------|
| CreateProcessW            | KERNEL32     | HIGH    | Process creation             |
| OpenProcessToken          | ADVAPI32     | HIGH    | Access process token         |
| GetTokenInformation       | ADVAPI32     | MEDIUM  | Query token privileges       |
| CreateWindowExW           | USER32       | LOW     | Window creation              |
| SendMessageW              | USER32       | LOW     | Window messaging             |
| PeekNamedPipe             | KERNEL32     | MEDIUM  | Pipe communication           |

## Extraction Priority

To understand the true malicious behavior, you MUST extract the Python payload:

1. **Use pyinstxtractor**: `python pyinstxtractor.py XBot.exe`
2. **Locate main script**: Usually named `XBot.pyc` or `__main__.pyc`
3. **Decompile bytecode**: `uncompyle6 XBot.pyc > XBot.py`
4. **Analyze Python source**: This contains the actual malware logic

## Indicators of Compromise (IOCs)

### File Indicators

```
Filename: XBot.exe
Type: PE64 executable
Packer: PyInstaller

Strings:
- "PyInstallerOnefileHiddenWindow"
- "PYINSTALLER_RESET_ENVIRONMENT"
- "_MEIPASS"
- "_pyinstaller_pyz"
```

### Runtime Indicators

```
Temp Directory: %TEMP%\_MEI<random>\
Hidden Window Class: PyInstallerOnefileHiddenWindow
Process Name: XBot.exe

Child Processes: May spawn additional executables via CreateProcessW
Network Activity: TCP/UDP socket connections (exact details in Python payload)
```

### Behavioral Indicators

- Creates temporary extraction directory
- Loads Python DLL (may be embedded)
- May check privilege levels via token APIs
- Displays error dialogs on failure (disguises as legitimate app)

## What the Bootloader Does (Step-by-Step)

```
1. [Entry Point] FUN_140001000
   └─> Initialize environment
   └─> Get command-line arguments

2. [Archive Location] Locate embedded PYZ archive
   └─> Read archive cookie (magic bytes)
   └─> Parse Table of Contents (TOC)

3. [Extraction] Extract to temp directory
   └─> Create %TEMP%\_MEI<random>\
   └─> Decompress files (zlib)
   └─> Extract Python interpreter (if embedded)
   └─> Extract Python modules and main script

4. [Python Init] Initialize Python runtime
   └─> Load Python DLL
   └─> Call Py_InitializeFromConfig
   └─> Setup sys.argv, __file__, __main__

5. [Execution] Run embedded Python script
   └─> Unmarshal bytecode
   └─> Execute via PyImport_ExecCodeModule
   └─> THE ACTUAL MALWARE RUNS HERE

6. [Cleanup] Finalize
   └─> Call Py_Finalize
   └─> Optionally cleanup temp files
   └─> Exit
```

## Risk Assessment

### High-Risk Indicators

- **Named "XBot"** - Naming convention suggests bot/RAT malware
- **Network capabilities** - C2 communication likely
- **Process creation** - Can spawn additional malware
- **Token manipulation** - May attempt privilege escalation
- **Hidden execution** - Designed to avoid detection

### Medium-Risk Indicators

- **PyInstaller packing** - Common in both legitimate and malicious software
- **Temp file extraction** - Standard PyInstaller behavior
- **Error dialogs** - May masquerade as legitimate application

## Recommended Next Steps

### For Malware Analysis

1. **PRIORITY 1**: Extract Python payload (see EXTRACTION_GUIDE.md)
2. Decompile Python bytecode to source
3. Static analysis of Python code for:
   - C2 server addresses
   - Keylogging functionality
   - Data exfiltration
   - Credential theft
   - Cryptocurrency mining
   - Ransomware behavior

4. Dynamic analysis in sandbox:
   - Network traffic capture (Wireshark)
   - File system monitoring (Process Monitor)
   - Registry changes (RegShot)
   - Process behavior (Process Explorer)

### For Detection

Create detection rules for:
- PyInstaller magic bytes + suspicious strings
- `_MEI*` directory creation in %TEMP%
- Python interpreter loaded by non-Python executables
- Network connections from PyInstaller executables
- Token manipulation by Python processes

### For Incident Response

If this file was executed on a system:

1. **Isolate** the system from network immediately
2. **Preserve** memory dump and disk image
3. **Check** for:
   - Persistence mechanisms (Registry Run keys, Scheduled Tasks)
   - Created user accounts
   - Modified system files
   - Outbound network connections
   - Data exfiltration
4. **Scan** for additional dropped files
5. **Review** event logs and network logs

## Questions to Answer with Python Payload Analysis

Once extracted, investigate:

- [ ] What C2 servers does it connect to?
- [ ] What data does it exfiltrate?
- [ ] Does it establish persistence?
- [ ] What credentials/data does it target?
- [ ] Does it have ransomware capabilities?
- [ ] Does it perform cryptocurrency mining?
- [ ] Does it download additional payloads?
- [ ] What keylogging/screen capture features exist?
- [ ] Does it spread laterally or self-replicate?

## Comparison: Bootloader vs. Payload

| Component  | What We Know                    | What We Need to Know           |
|------------|---------------------------------|--------------------------------|
| Bootloader | PyInstaller (ANALYZED)          | N/A - Standard PyInstaller     |
| Payload    | Python script (NOT YET SEEN)    | CRITICAL - Contains malware    |

**Current Status**: We have analyzed the wrapper (bootloader) but NOT the actual malicious code (Python payload).

**The bootloader is like analyzing the envelope of a letter - we need to extract and read the letter itself.**

## Tools Required for Further Analysis

```bash
# Extraction
pip install pyinstxtractor

# Decompilation
pip install uncompyle6
pip install decompyle3

# Analysis
pip install yara-python
pip install pefile
pip install oletools

# Monitoring (Windows)
- Process Monitor (procmon.exe)
- Process Explorer (procexp.exe)
- Wireshark
- x64dbg or WinDbg
```

## Conclusion

XBot.exe is a **PyInstaller-packaged Python application** with strong indicators of malicious intent. The decompiled C code reveals only the bootloader mechanism - the actual malicious functionality resides in the embedded Python script that must be extracted and analyzed separately.

**This is almost certainly malware. Do not execute outside of an isolated analysis environment.**

---

**Analysis Status**: Phase 1 Complete (Bootloader Analysis)
**Next Phase**: Python Payload Extraction & Analysis (REQUIRED)
**Overall Completeness**: 40% - Bootloader understood, payload unknown
