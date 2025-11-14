# Getting XBot Python Source Code

This guide shows you how to get actual Python source code from XBot.pyc for defensive analysis.

## Quick Start (Best Method)

```bash
# On your Mac, run this script
cd "/Users/aderdesouza/Desktop/XBot v2.1/XBot.exe_extracted"
python3 ~/Xbot/decompile_xbot.py XBot.pyc ./decompiled

# This will try all decompilation methods automatically
```

---

## Method 1: pycdc (BEST - Supports Python 3.13)

### Install pycdc on macOS

#### Option A: Using Homebrew (Easiest)

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Try to install pycdc
brew install pycdc
```

If brew doesn't have pycdc, use Option B:

#### Option B: Build from Source

```bash
# Install CMake if needed
brew install cmake

# Clone pycdc repository
cd ~/Downloads
git clone https://github.com/zrax/pycdc.git
cd pycdc

# Build it
cmake .
make

# Test it
./pycdc --version

# Decompile XBot
./pycdc "/Users/aderdesouza/Desktop/XBot v2.1/XBot.exe_extracted/XBot.pyc" > XBot.py
```

#### Option C: Download Pre-built Binary

```bash
# Download latest release
cd ~/Downloads
curl -L -O https://github.com/zrax/pycdc/releases/latest/download/pycdc-darwin

# Make executable
chmod +x pycdc-darwin

# Decompile
./pycdc-darwin "/Users/aderdesouza/Desktop/XBot v2.1/XBot.exe_extracted/XBot.pyc" > XBot.py
```

### If pycdc Works

You'll get **clean Python source code** like:

```python
from datetime import datetime, timedelta
import keyring
from playwright.async_api import async_playwright
import aiohttp

class XBotApp:
    def __init__(self, page):
        self.page = page
        self.settings = {
            'drop_limit': 50,
            'drop_sleep': 5,
            'drop_message': 'Hit my pinned post\nPlease add me to your groups'
        }

    async def _run_automation(self, profile):
        # Actual implementation code here
        for target in targets:
            await self.post_message(target)
            await asyncio.sleep(self.settings['drop_sleep'])
```

---

## Method 2: Use the Automated Script

```bash
# Run the comprehensive decompiler
python3 decompile_xbot.py XBot.pyc

# It will try:
# 1. pycdc (best chance)
# 2. uncompyle6
# 3. decompyle3
# 4. Manual reconstruction
# 5. Hybrid analysis
```

Check the `./decompiled/` directory for results.

---

## Method 3: Manual Bytecode Analysis

If decompilers fail, you can manually analyze the bytecode:

### Step 1: Generate Detailed Disassembly

```python
python3 -c "
import dis
import marshal

with open('XBot.pyc', 'rb') as f:
    f.read(16)  # Skip header
    code = marshal.load(f)
    dis.dis(code)
" > XBot_disassembly.txt
```

### Step 2: Read the Disassembly

```bash
# The disassembly shows bytecode instructions
cat XBot_disassembly.txt
```

Example bytecode:
```
  0 LOAD_CONST     0 ('XBot V2.1')
  2 STORE_NAME     1 (version)
  4 LOAD_NAME      2 (keyring)
  6 LOAD_METHOD    3 (get_password)
  8 LOAD_CONST     4 ('XBot')
 10 LOAD_CONST     5 ('client_id')
 12 CALL_METHOD    2
 14 STORE_NAME     6 (client_id)
```

**Translation:**
```python
version = 'XBot V2.1'
client_id = keyring.get_password('XBot', 'client_id')
```

### Step 3: Reconstruct Logic Manually

Use my hybrid analysis script output as a template, then fill in details from disassembly.

---

## What You'll Get

### If pycdc Works (Best Case):

✅ **Complete, working Python source code**
- All class definitions
- All function implementations
- All logic and algorithms
- Editable and runnable

### If pycdc Fails (Fallback):

✅ **Hybrid Analysis** (very readable):
- Class structure
- Function signatures
- Configuration values
- Program flow
- Pseudocode of main logic

✅ **Bytecode Disassembly** (technical):
- Every instruction
- Exact program behavior
- Can be manually translated

---

## Understanding the Output

### Hybrid Analysis Structure

```python
# Configuration
DEFAULT_SETTINGS = {
    "drop_limit": 50,
    "drop_sleep": 5,
    # ... all settings documented
}

# Main class
class XBotApp:
    def __init__(self, page):
        # What it does documented

    async def _run_automation(self, profile):
        """
        Documented behavior:
        1. Login to Twitter
        2. Get target list
        3. For each target:
           - Post message
           - Sleep
        """
```

### Function Mapping

From bytecode analysis, you'll know:

| Function | Purpose | Key Operations |
|----------|---------|----------------|
| `_run_automation()` | Main spam loop | Playwright automation, message posting |
| `_load_profiles_local()` | Load credentials | Read .xbot_profiles.json |
| `_save_settings_local()` | Save config | Write .settings.json |
| `_toggle_run()` | Start/stop bot | Create/cancel async tasks |
| `_show_settings_dialog()` | Settings UI | Flet GUI controls |
| `get_password()` | Get credentials | Keyring.get_password() |

---

## For Defensive Analysis

### What You Need to Understand:

1. **Attack Vectors**
   ```python
   # From source/analysis, you'll see:
   - How it logs into Twitter (Playwright browser automation)
   - How it evades rate limits (sleep intervals, randomization)
   - How it selects targets (group lists, user lists)
   - How it posts messages (browser automation clicks)
   ```

2. **Detection Points**
   ```python
   # You can detect:
   - File creation: .xbot_profiles.json, .settings.json
   - Process: playwright browser processes
   - Network: Twitter.com automated access patterns
   - Registry: Windows Credential Manager access
   ```

3. **Defense Strategies**
   ```python
   # Based on understanding the code:
   - Monitor for rapid Twitter posting patterns
   - Detect identical messages
   - Watch for browser automation (Playwright)
   - Check for suspicious sleep/delay patterns
   - Monitor credential access patterns
   ```

4. **Mitigation**
   ```python
   # Twitter platform level:
   - Rate limiting enforcement
   - Message similarity detection
   - Browser automation detection
   - CAPTCHA challenges
   ```

---

## Recommended Workflow

### Day 1: Get the Code

```bash
# Try pycdc first
brew install cmake
git clone https://github.com/zrax/pycdc.git
cd pycdc && cmake . && make
./pycdc ~/XBot.pyc > XBot_source.py

# If that fails, use my script
python3 decompile_xbot.py ~/XBot.pyc
```

### Day 2: Analyze Automation Logic

Focus on:
```bash
# Find the main automation function
grep -A 50 "_run_automation" XBot_source.py

# Find credential handling
grep -A 20 "keyring\|password\|CLIENT_ID" XBot_source.py

# Find rate limiting
grep -A 10 "sleep\|delay\|rate_limit" XBot_source.py
```

### Day 3: Study Evasion Techniques

```bash
# Find detection avoidance
grep -A 10 "leniency\|skip\|evade" XBot_source.py

# Find randomization
grep -A 10 "random" XBot_source.py
```

### Day 4: Build Defenses

Based on what you learned:
1. Create detection signatures
2. Build monitoring rules
3. Implement rate limiting
4. Deploy countermeasures

---

## Troubleshooting

### "pycdc: command not found"

```bash
# Check if it's installed
which pycdc

# If not, build from source (see Option B above)
```

### "pycdc failed to decompile"

Try the fallback methods:
```bash
# Use my automated script
python3 decompile_xbot.py XBot.pyc

# Check hybrid analysis output
cat decompiled/XBot_hybrid_analysis.py
```

### "I need more detail than hybrid analysis"

Manually translate bytecode:
```bash
# Generate detailed disassembly
python3 analyze_xbot_bytecode.py XBot.pyc ./output

# Read the disassembly
cat output/XBot_disassembly.txt

# Translate opcodes to Python manually
# Example:
# LOAD_CONST 'hello' → variable = 'hello'
# CALL_METHOD 2      → function(arg1, arg2)
# STORE_NAME x       → x = result
```

---

## Expected Results

### Best Case (pycdc works):

You get a file like:
```python
# XBot.py (5000+ lines of clean Python code)
# Fully functional, editable source

from datetime import datetime
import keyring
from playwright.async_api import async_playwright

class XBotApp:
    # ... complete implementation

    async def _run_automation(self, profile):
        browser = await async_playwright().start()
        # ... actual automation code
```

### Good Case (hybrid analysis):

You get:
```python
# XBot_hybrid_analysis.py (1000+ lines)
# Structure + documentation + pseudocode

class XBotApp:
    """Documented behavior"""

    async def _run_automation(self, profile):
        """
        Known behavior:
        1. Opens Playwright browser
        2. Logs into Twitter
        3. Iterates through targets
        4. Posts messages with delays
        """
        # Implementation details from bytecode analysis
```

### Minimum Case (disassembly only):

You get:
```
# Bytecode instructions (technical)
0 LOAD_CONST     'XBot'
2 STORE_NAME     name
# ... (requires manual translation)
```

---

## Next Steps

Once you have the source code (in any form):

1. **Study the automation flow**
   - How it logs in
   - How it selects targets
   - How it posts messages

2. **Identify attack patterns**
   - Timing characteristics
   - Message patterns
   - Behavioral signatures

3. **Build detection**
   - YARA rules (already provided)
   - Behavior-based detection
   - Network signatures

4. **Create defenses**
   - Platform-level (Twitter)
   - Network-level (monitoring)
   - Endpoint-level (EDR rules)

5. **Document findings**
   - Write defense playbook
   - Create incident response plan
   - Share threat intelligence

---

## Files You'll Have

After running all methods:

```
decompiled/
├── XBot_pycdc.py              # Clean source (if pycdc works)
├── XBot_hybrid_analysis.py     # Readable structure + logic
├── XBot_reconstructed.py       # Bytecode + pseudocode
└── XBot_disassembly.txt        # Raw bytecode (if manual)
```

Use whichever is most complete for your defensive analysis.

---

**Start here:**
```bash
python3 decompile_xbot.py "/Users/aderdesouza/Desktop/XBot v2.1/XBot.exe_extracted/XBot.pyc"
```

This will try everything and give you the best possible result.
