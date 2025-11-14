# Reverse Engineering Analysis: XBot.exe

## Executive Summary

The analyzed executable (`XBot.exe`) is a **PyInstaller-packaged Windows executable** (64-bit PE format). PyInstaller is a legitimate tool used to bundle Python applications into standalone executables. This analysis examines the bootloader stub and embedded components.

**WARNING**: This file appears to be named "XBot" which suggests potential malicious intent. Exercise extreme caution when handling this executable.

## File Information

- **Format**: PE64 (Portable Executable 64-bit)
- **Platform**: Windows x64
- **Packer**: PyInstaller (Python to EXE converter)
- **Decompiler**: Ghidra (based on output format)
- **Architecture**: x86-64

## PE Structure

### Sections Identified

```
.text    - Executable code (bootloader)
.rdata   - Read-only data (strings, constants)
.data    - Initialized data
.pdata   - Exception handling data
.fptable - Function pointer table
.rsrc    - Resources (likely contains Python archive)
.reloc   - Relocation table
```

## PyInstaller Architecture

### 1. Bootloader Component

The decompiled C code represents the PyInstaller bootloader, which is responsible for:

- Extracting embedded Python interpreter
- Decompressing archived Python modules
- Initializing the Python runtime
- Executing the main Python script

### 2. Key Functions Identified

#### Archive Extraction Functions

Located around `c:140001050` - Functions that extract files from embedded archives:

```c
// Failed to extract messages indicate extraction functionality
"Failed to extract %s: failed to open"
"Failed to extract %s: failed to seek"
"Failed to extract %s: failed to allocate"
"Failed to extract %s: inflateInit failed"
"Failed to extract %s: decompress failed"
```

**Purpose**: Extracts Python bytecode (.pyc files), modules, and dependencies from the embedded PYZ archive.

#### Python Initialization Functions

References to Python C API functions found:

```
Py_InitializeFromConfig  - Initialize Python interpreter
Py_Finalize             - Shutdown Python interpreter
PyImport_AddModule      - Import Python modules
PyImport_ExecCodeModule - Execute compiled Python code
PyImport_ImportModule   - Import module by name
PyRun_SimpleStringFlags - Run Python code from string
```

**Location**: Functions around `c:140005830` handle Python API imports.

#### Process Creation

Found at `c:140008d1e`:
```c
CreateProcessW  - Creates new Windows processes
```

**Implication**: The embedded Python script can spawn additional processes.

### 3. Environment Variables

PyInstaller-specific environment variables detected:

```
PYINSTALLER_RESET_ENVIRONMENT     - Controls environment cleanup
PYINSTALLER_STRICT_UNPACK_MODE    - Archive extraction mode
PYINSTALLER_SUPPRESS_SPLASH_SCREEN - GUI splash control
_MEIPASS                          - Temporary extraction directory
_MEI%d                            - Temp directory naming pattern
```

### 4. Archive Structure

The executable contains a **PYZ archive** (PyInstaller's compressed archive format):

- **Cookie**: Magic bytes identifying PyInstaller archive
- **TOC** (Table of Contents): Index of embedded files
- **Compressed Data**: zlib-compressed Python bytecode and modules

Error messages reveal the archive format:
```
"Could not read full TOC!"
"PYZ archive entry not found in the TOC!"
"Failed to format PYZ archive path"
```

## Execution Flow

### Stage 1: Bootloader Startup

1. Entry point at `FUN_140001000` (c:325)
2. Initializes runtime environment
3. Retrieves command-line arguments via `_get_wide_winmain_command_line`

### Stage 2: Archive Extraction

1. Locates embedded PYZ archive at end of executable
2. Reads archive cookie and TOC
3. Extracts files to temporary directory (`_MEIPASS`)
4. Decompresses Python modules using zlib (inflate)

### Stage 3: Python Initialization

1. Loads Python DLL (embedded or system)
2. Calls `Py_InitializeFromConfig`
3. Sets up `sys.argv` with command-line arguments
4. Sets `__file__` and `__main__` module

### Stage 4: Script Execution

1. Locates main Python script in archive
2. Unmarshals Python bytecode objects
3. Executes via `PyImport_ExecCodeModule`
4. Handles exceptions and displays error dialogs if needed

### Stage 5: Cleanup

1. Runs embedded script to completion
2. Calls `Py_Finalize` to shutdown Python
3. Optionally cleans up temporary files

## Security-Relevant Observations

### 1. Process Token Manipulation

Found references to `OpenProcessToken` and `GetTokenInformation` (c:1400087a3):

```c
OpenProcessToken      - Opens access token of a process
GetTokenInformation   - Retrieves token information
```

**Concern**: May be checking or elevating privileges.

### 2. Hidden Window Creation

At `c:140008d54`:
```
"PyInstallerOnefileHiddenWindow"
"PyInstaller Onefile Hidden Window"
```

**Purpose**: Creates hidden window for message handling (common in GUI-less applications).

### 3. Error Handling & Dialogs

The bootloader creates error dialogs:
```
"Unhandled exception in script"
"Failed to execute script '%ls'"
```

**Note**: Displays GUI dialogs on errors, suggesting this may masquerade as a legitimate application.

### 4. Network Capabilities

Found socket-related error strings:
```
"connection already in progress"
"connection aborted"
"connection refused"
"connection reset"
"not connected"
```

**Implication**: The embedded Python script likely performs network operations.

## How to Extract the Python Payload

To analyze the actual malicious Python code:

### Method 1: PyInstaller Extractor

```bash
# Use pyinstxtractor
python pyinstxtractor.py XBot.exe

# This will extract:
# - PYZ archive
# - Compiled Python modules (.pyc files)
# - Main script
```

### Method 2: Manual Extraction

1. **Locate Archive**: Search for PyInstaller magic cookie at end of file
2. **Parse TOC**: Read table of contents structure
3. **Extract Files**: Decompress zlib-compressed entries
4. **Decompile PYC**: Use `uncompyle6` or `decompyle3` on .pyc files

### Method 3: Runtime Analysis

```bash
# Monitor file system access
# PyInstaller extracts to: %TEMP%\_MEI<random>

# Monitor in debugger and break at:
# - Py_InitializeFromConfig
# - PyImport_ExecCodeModule
```

## Indicators of Compromise (IOCs)

### File Characteristics

- **Executable Name**: `XBot.exe`
- **Bootloader**: PyInstaller (likely version 4.x or 5.x based on structure)
- **Hidden Window Class**: `PyInstallerOnefileHiddenWindow`

### Behavioral Indicators

- Creates hidden windows
- Extracts files to `%TEMP%\_MEI*` directories
- May check process tokens/privileges
- Performs network operations (sockets)
- Spawns child processes via `CreateProcessW`

### String Artifacts

```
PYINSTALLER_RESET_ENVIRONMENT
_MEIPASS
_pyinstaller_pyz
PyInstallerOnefileHiddenWindow
```

## Recommendations

### For Analysis

1. **Extract Python payload** using pyinstxtractor
2. **Decompile .pyc files** to readable Python source
3. **Analyze network behavior** in isolated environment
4. **Monitor process creation** and file system operations
5. **Check for anti-analysis techniques** in Python code

### For Detection

1. **YARA Rules**: Detect PyInstaller magic bytes and TOC structure
2. **Behavioral Monitoring**: Watch for `_MEI*` directory creation in %TEMP%
3. **Network Monitoring**: Monitor network connections from Python processes
4. **Sandbox Execution**: Run in isolated environment to observe full behavior

### For Mitigation

1. **DO NOT EXECUTE** on production systems
2. **Isolate Sample**: Keep in password-protected archive
3. **Report**: Submit to antivirus vendors and threat intelligence platforms
4. **Block IOCs**: Add hash to block lists

## Technical Details

### PE Imports (Key DLLs)

```
KERNEL32.DLL - Core Windows APIs (CreateProcessW, PeekNamedPipe, MulDiv)
USER32.DLL   - GUI functions (CreateWindowExW, SendMessageW)
ADVAPI32.DLL - Security APIs (OpenProcessToken, GetTokenInformation)
GDI32.DLL    - Graphics (CreateFontIndirectW)
COMCTL32.DLL - Common controls
```

### Compression

Uses **zlib** (inflate/deflate) for archive compression:
```
"inflateInit failed"
"decompress failed"
```

Version string found: `"1.3.1"` (likely zlib version)

## Conclusion

This executable is a PyInstaller-packaged Python application. The bootloader itself is legitimate PyInstaller code, but the embedded Python script is the actual payload that requires analysis.

The presence of:
- Network operations
- Process creation capabilities
- Token manipulation
- Hidden windows
- Name "XBot"

...suggests this is likely **malware** (possibly a Remote Access Trojan, information stealer, or bot).

**Next Steps**: Extract and decompile the Python payload to determine exact functionality and malicious behavior.

---

**Analysis Date**: 2025-11-14
**Analyst**: Automated Reverse Engineering Analysis
**Decompiler**: Ghidra
**File Size**: 9.5MB (decompiled C source)
