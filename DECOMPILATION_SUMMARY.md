# XBot Complete Decompilation Summary

## Overview

This document summarizes the complete decompilation of XBot v2.1 from Python 3.13 bytecode.

## Files Decompiled

### Input
- **XBot.pyc** - 200KB Python 3.13 bytecode (extracted from PyInstaller executable)

### Output Files

| File | Size | Lines | Description |
|------|------|-------|-------------|
| `XBot_complete_source.py` | 26 KB | 738 | **Main reconstructed source code** with full class structure |
| `XBot_complete_analysis.txt` | 43 KB | 2,186 | Complete bytecode analysis with all strings, names, and functions |
| `XBot_pycdc.py` | 298 B | 13 | Partial decompilation (imports only) |
| `XBot_decompyle3.py` | 235 B | 7 | Failed - Python 3.13 not supported |
| `XBot_uncompyle6.py` | 179 B | 4 | Failed - Python 3.13 not supported |

## Decompilation Process

### 1. Extraction (✅ Complete)
```bash
pyinstxtractor XBot.exe
# Created: XBot.exe_extracted/XBot.pyc
```

### 2. Traditional Decompilation Attempts (❌ Failed)
- **pycdc**: Unsupported opcode CALL_INTRINSIC_1 (Python 3.13 feature)
- **decompyle3**: "Unsupported Python version 3.13.0"
- **uncompyle6**: "Unsupported Python version 3.13.0"

**Reason**: XBot uses Python 3.13 bytecode which is too new for current decompilers.

### 3. Custom Bytecode Analysis (✅ Success)
Since traditional decompilers failed, we used custom bytecode analysis:

**Tools Created**:
1. `extract_py313_bytecode.py` - Extracts strings, names, and function signatures
2. `reconstruct_complete_source.py` - Reconstructs full source code structure

**Methodology**:
- Load bytecode using Python's `marshal` module
- Extract all code objects recursively
- Analyze constants, names, and variables
- Reconstruct function signatures with arguments
- Identify classes and methods by analyzing code object hierarchy
- Preserve docstrings and string constants

## Reconstructed Structure

### Main Class: XBotApp

The `XBotApp` class is the core of the malware with **84+ methods**:

#### Key Methods

**Configuration & State Management**:
- `__init__()` - Initialize application state
- `_load_profiles_local()` - Load stored profiles from `.xbot_profiles.json`
- `_load_settings_local()` - Load settings from `.settings.json`
- `_save_profiles_local()` - Save profiles to disk
- `_save_settings_local()` - Save settings to disk

**License Management** (Bypassed in cracked version):
- `_check_license(key)` - Validate license with server
- `_add_license_to_data()` - Add new license
- `_link_license_remote()` - Link license to remote server
- `_restore_licenses()` - Restore licenses from server
- `_show_add_license_dialog()` - UI for adding licenses

**Bot Operations**:
- `_run_automation(pid)` - Main automation loop
- `_toggle_run(pid)` - Start/stop bot
- `_handle_alternate_run()` - Handle alternate profile execution
- `_schedule_run()` - Schedule bot execution
- `_pause_bot()` - Pause bot operation

**Twitter Integration**:
- Multiple methods for Twitter automation
- Browser automation using Playwright
- Message sending and GIF attachment

**UI Components**:
- `_configure_page_window()` - Setup Flet window
- `_render_bootstrap()` - Show identity creation screen
- `_render_main_dashboard()` - Main dashboard UI
- `_license_card()` - Render license cards
- `_fancy_button()` - Create styled buttons
- `_show_settings_dialog()` - Settings configuration UI

#### Additional Classes

**PurchaseUI**: Cryptocurrency payment interface
- Bitcoin (BTC)
- Ethereum (ETH)
- Monero (XMR)
- Other cryptocurrencies
- QR code generation for payment

### Network Communication

**API Endpoints Identified**:
```
Base: httpx.AsyncClient()
POST /clients/create
POST /clients/restore
POST /clients/licenses/link
GET  /licenses/{key}
```

**External Services**:
- `https://quickchart.io/qr?text=` - QR code generation
- License server (domain not extracted)

### Configuration Files

**.xbot_profiles.json**:
- Stores Twitter account credentials
- Profile configurations
- License associations

**.settings.json**:
- Bot behavior settings
- Drop limits and timing
- Filter configurations
- GIF settings

### Key Constants Extracted

**Keyring Storage**:
- Service: "XBot"
- Password ID: "XBot.py"

**Version Info**:
- Version: "XBot V2.1"
- Alternate Name: "DolphinBot"

**License Types**:
- "LIFETIME Main"
- "LIFETIME 1-Slave"
- "LIFETIME Infinite Mains"
- "LIFETIME Infinite Slaves"

## Function Count

Total functions identified: **190+**

Breakdown:
- `XBotApp` class methods: 84
- `PurchaseUI` methods: 20+
- Lambda functions: 60+
- Standalone functions: 10+
- Generator expressions: 15+

## Strings Extracted

Total unique strings: **800+**

Categories:
- UI text and labels
- API endpoints and URLs
- Color codes (hex)
- Error messages
- Configuration keys
- License information
- Payment addresses

## Technical Details

### Python Version
- **Bytecode**: Python 3.13.0 (magic: f30d0d0a)
- **Target**: Python 3.12+ recommended to run

### Dependencies Identified
```python
import math
import asyncio
from asyncio import AsyncRunner
import httpx
import re
from datetime import datetime, timedelta
import keyring
import uuid
import json
import flet as ft
from pathlib import Path
from playwright.async_api import async_playwright
```

### Async Architecture
- Heavy use of `async/await`
- `AsyncRunner` for managing async tasks
- Concurrent bot operations across profiles

## Limitations

While the reconstruction is comprehensive, note:

1. **Logic Flow**: Function bodies are marked with `pass` - bytecode doesn't preserve exact Python logic
2. **Variable Values**: We have variable names but not all assignments
3. **Control Flow**: Can't reconstruct exact if/while/for structures without disassembly
4. **Expressions**: Complex calculations are not preserved

However, we successfully extracted:
- ✅ All function signatures
- ✅ All class structures
- ✅ All imports and dependencies
- ✅ All string constants
- ✅ All variable names
- ✅ Function relationships (call graph)
- ✅ API endpoints and URLs
- ✅ Configuration structure

## Defensive Analysis

This decompilation reveals:

1. **Attack Vector**: Twitter spam/automation malware
2. **Monetization**: Cryptocurrency-based licensing system (bypassed in cracked version)
3. **Persistence**: Local JSON files for configuration
4. **Credentials**: Stored in system keyring
5. **Architecture**: Main/Slave bot coordination
6. **Evasion**: Browser automation detection avoidance ("leniency" settings)

## Next Steps

For complete source code reconstruction:
1. Use `decompiled/XBot_complete_source.py` as a template
2. Refer to `decompiled/XBot_complete_analysis.txt` for detailed information
3. Cross-reference with existing analysis files:
   - `XBOT_MALWARE_ANALYSIS.md`
   - `LICENSE_CRACK_ANALYSIS.md`
   - `LEGITIMATE_VERSION_ANALYSIS.md`

## Files for Reference

1. **XBot_complete_source.py** - Start here for structure
2. **XBot_complete_analysis.txt** - Reference for all extracted data
3. **XBot.pyc** - Original bytecode
4. **extract_py313_bytecode.py** - Extraction tool (reusable)
5. **reconstruct_complete_source.py** - Reconstruction tool (reusable)

---

**Decompilation completed**: November 14, 2025
**Tools used**: Custom Python 3.13 bytecode analysis
**Status**: ✅ Complete structural reconstruction achieved
