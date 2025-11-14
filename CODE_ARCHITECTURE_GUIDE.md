# XBot Code Architecture - Where Logic Goes

This explains the program structure and where each type of functionality is implemented.

## 🏗️ Overall Architecture

```
XBotApp (Main Class)
├── Initialization & Setup
├── UI Rendering & Controls
├── License Management
├── Profile Management
├── Bot Automation Engine ← Core spam logic here
├── Settings & Configuration
└── File I/O Operations
```

---

## 📍 Function Map - What Goes Where

### 1. INITIALIZATION & SETUP

**Function:** `__init__(self)`
**Location:** Line ~43 in XBot_complete_source.py

**Logic That Goes Here:**
```python
def __init__(self, page):
    # Set up instance variables
    self.page = page
    self.runner = AsyncRunner()
    self.saved_profiles = {}
    self.accounts = []  # License + profile data
    self.states = {}    # Per-profile runtime state
    self.all_settings = DEFAULT_SETTINGS.copy()

    # Initialize UI state
    self.license_column = None
    self.show_keys = False

    # Load saved data from disk
    self._load_profiles_local()
    self._load_settings_local()
```

**What It Does:**
- Creates the app object
- Sets up empty data structures
- Loads saved profiles/settings from JSON files

---

### 2. CONFIGURATION LOADING/SAVING

#### A. Load Profiles

**Function:** `_load_profiles_local(self)`
**Location:** Line ~534 in XBot_complete_source.py

**Logic That Goes Here:**
```python
def _load_profiles_local(self):
    # Check if file exists
    if not os.path.exists('.xbot_profiles.json'):
        return

    # Read file
    with open('.xbot_profiles.json', 'r') as f:
        data = json.load(f)

    # Parse structure: {'licenses': [...]}
    for license_entry in data.get('licenses', []):
        key = license_entry['key']
        browser_id = license_entry.get('browser_id')
        model = license_entry.get('model')

        # Store in self.accounts
        self.accounts.append({
            'key': key,
            'browser_id': browser_id,
            'model': model,
            'profiles': license_entry.get('profiles', [])
        })
```

**What It Does:**
- Reads `.xbot_profiles.json`
- Parses license data
- Populates `self.accounts` array

#### B. Save Profiles

**Function:** `_save_profiles_local(self)`
**Location:** Line ~521 in XBot_complete_source.py

**Logic That Goes Here:**
```python
def _save_profiles_local(self):
    # Build data structure
    data = {
        'licenses': []
    }

    # Convert self.accounts to JSON format
    for lic in self.accounts:
        data['licenses'].append({
            'key': lic['key'],
            'browser_id': lic.get('browser_id'),
            'model': lic.get('model'),
            'profiles': lic.get('profiles', [])
        })

    # Write to disk
    with open('.xbot_profiles.json', 'w') as f:
        json.dump(data, f, indent=2)
```

**What It Does:**
- Converts in-memory data to JSON
- Writes to `.xbot_profiles.json`

---

### 3. LICENSE VALIDATION

**Function:** `_check_license(self, key)`
**Location:** Line ~62 in XBot_complete_source.py

**Logic That Goes Here:**
```python
async def _check_license(self, key):
    # Create HTTP client
    async with httpx.AsyncClient() as client:
        # Make API request
        url = f"{API_BASE}/licenses/{key}"
        response = await client.get(url)

        # Check status
        if response.status_code == 200:
            data = response.json()
            # Returns: {'valid': true/false, 'type': 'LIFETIME', 'expires': null}
            return data
        else:
            return None
```

**What It Does:**
- HTTP GET to license server
- Validates license key
- Returns license info (type, expiration)

**Network Call:**
```
GET https://api.xbot-server.com/licenses/XXXX-XXXX-XXXX
Response: {"valid": true, "type": "LIFETIME Main", "expires": null}
```

---

### 4. UI RENDERING

#### A. Main Dashboard

**Function:** `_render_main_dashboard(self)`
**Location:** Line ~695 in XBot_complete_source.py

**Logic That Goes Here:**
```python
def _render_main_dashboard(self):
    # Create page layout
    self.page.clean()  # Clear existing UI

    # Build license cards column
    license_cards = []
    for i, lic in enumerate(self.accounts):
        card = self._license_card(lic, i)
        license_cards.append(card)

    # Create layout
    main_view = ft.Column([
        ft.Text("XBot V2.1", size=24),
        ft.Divider(),
        ft.Column(license_cards),  # All licenses
        ft.Row([
            self._fancy_button("Add License", ...),
            self._fancy_button("Settings", ...)
        ])
    ])

    # Add to page
    self.page.add(main_view)
    self.page.update()
```

**What It Does:**
- Clears screen
- Creates license cards UI
- Adds buttons and controls
- Renders to window

#### B. License Card

**Function:** `_license_card(self, lic, index)`
**Location:** Line ~110 in XBot_complete_source.py

**Logic That Goes Here:**
```python
def _license_card(self, lic, index):
    # Extract license data
    key = lic['key']
    profiles = lic.get('profiles', [])

    # Create expandable card
    card = ft.Container(
        content=ft.Column([
            # Header: License key + expand button
            ft.Row([
                ft.Text(f"License: {key[:8]}..."),
                ft.IconButton(icon=ft.icons.EXPAND_MORE)
            ]),

            # Profiles list (hidden by default)
            ft.Column([
                self._profile_row(p) for p in profiles
            ], visible=False),

            # Add profile button
            ft.Button("Add Profile", on_click=lambda e: self._add_profile(lic))
        ]),
        bgcolor="#1E2125",
        padding=10
    )

    return card
```

**What It Does:**
- Creates a UI card for each license
- Shows license key (masked)
- Lists profiles under that license
- Add profile button

---

### 5. BOT AUTOMATION ENGINE (CORE LOGIC)

#### A. Main Automation Loop

**Function:** `_run_automation(self, pid)`
**Location:** Would be implemented (currently `pass`)

**Logic That Goes Here:**
```
PSEUDOCODE (Not actual Python):

1. Get profile data from self.saved_profiles[pid]
   - Extract: username, email, password

2. Get settings from self.all_settings
   - drop_limit: how many messages to send
   - drop_sleep: delay between messages
   - drop_message: spam text
   - gif_keyword: GIF search term

3. Launch browser automation
   - Use Playwright to open Chrome
   - Set user agent to avoid detection

4. Login to Twitter
   - Navigate to twitter.com/login
   - Enter credentials
   - Handle 2FA if needed

5. Main spam loop (repeat drop_limit times):
   a. Find next target
      - Parse followers list
      - Or search for groups
      - Apply skip filters

   b. Navigate to target's DM
      - Click message button
      - Wait for DM window

   c. Compose message
      - Type drop_message into textarea

   d. Attach GIF (if no_gif = False)
      - Search GIPHY for gif_keyword
      - Pick random result if randomize=True
      - Attach to message

   e. Send message
      - Click send button
      - Wait for confirmation

   f. Update status
      - Increment drop_count
      - Update UI: "Sent 5/50"

   g. Sleep
      - Wait drop_sleep seconds
      - Randomize slightly if leniency enabled

   h. Check for rate limit
      - If Twitter shows warning
      - Sleep rate_limit_sleep seconds

6. Cleanup
   - Close browser
   - Update status: "Complete"
```

**Key Variables Used:**
- `pid`: Profile ID being automated
- `drop_count`: Messages sent so far
- `drop_limit`: Maximum messages to send
- `browser`: Playwright browser instance
- `page`: Playwright page instance

---

#### B. Target Selection

**Function:** Would be in helper methods called by `_run_automation`

**Logic That Goes Here:**
```
PSEUDOCODE:

def get_next_target():
    1. Get list of potential targets
       - From followers list
       - Or from group members

    2. Apply filters (from settings):
       - skip_chudai: Skip certain keywords
       - skip_missing_followers: Skip low follower count
       - skip_non_of_link: Skip if no OnlyFans link

    3. Check group_skip list
       - If user is in skip list, skip them

    4. Return next valid target username
```

---

#### C. Browser Interaction

**Functions:** Multiple helper methods

**Logic Distribution:**

```python
# Login flow
async def _login_twitter(self, page, username, password):
    # Navigate to login page
    # Fill username field
    # Fill password field
    # Click login button
    # Wait for home page
    pass

# Send DM
async def _send_dm(self, page, target_username, message, gif_url=None):
    # Navigate to target profile
    # Click message button
    # Type message
    # Attach GIF if provided
    # Click send
    # Wait for confirmation
    pass

# Search GIF
async def _search_gif(self, keyword, randomize=True):
    # Use Twitter's built-in GIF search
    # Search for keyword
    # Get results list
    # Pick random or first result
    # Return GIF URL
    pass
```

---

### 6. STATE MANAGEMENT

**Function:** `_ensure_pid_state(self, pid)`
**Location:** Line ~73 in XBot_complete_source.py

**Logic That Goes Here:**
```python
def _ensure_pid_state(self, pid):
    # Check if state exists
    if pid not in self.states:
        # Create new state object
        self.states[pid] = {
            'paused': False,          # Is bot paused?
            'error': None,            # Error message if failed
            'runtime_task': None,     # Async task reference
            'anim_task': None,        # UI animation task
            'scheduled': False,       # Is scheduled to run?
            'cancel_scheduled': False,
            'scheduled_task': None,
            'scheduled_start_time': None,
            'runtime': 0,             # Seconds running
            'drop_count': 0,          # Messages sent
        }

    return self.states[pid]
```

**What It Does:**
- Creates tracking state for each profile
- Stores: pause status, errors, task references, counters

---

### 7. RUN/PAUSE CONTROLS

**Function:** `_toggle_run(self, pid)`
**Location:** Would be implemented

**Logic That Goes Here:**
```python
async def _toggle_run(self, pid):
    # Get state
    state = self._ensure_pid_state(pid)

    # Check if already running
    if state['runtime_task'] is not None:
        # STOP the bot
        state['runtime_task'].cancel()
        state['runtime_task'] = None

        # Update UI
        self._update_status_ui(pid, "Stopped")
    else:
        # START the bot

        # Get profile data
        profile = self._get_profile_by_id(pid)

        # Create async task
        state['runtime_task'] = asyncio.create_task(
            self._run_automation(pid)
        )

        # Update UI
        self._update_status_ui(pid, "Running...")
```

**What It Does:**
- Toggles bot on/off for a profile
- Creates/cancels async task
- Updates UI button state

---

### 8. SETTINGS DIALOG

**Function:** `_show_settings_dialog(self, pid)`
**Location:** Line ~658 in XBot_complete_source.py

**Logic That Goes Here:**
```python
def _show_settings_dialog(self, pid):
    # Get current settings
    settings = self.all_settings.copy()

    # Create dialog with input fields
    dialog = ft.AlertDialog(
        title=ft.Text("Settings"),
        content=ft.Column([
            # Drop limit
            ft.TextField(
                label="Drop Limit",
                value=str(settings['drop_limit']),
                on_change=lambda e: settings.update({'drop_limit': int(e.control.value)})
            ),

            # Drop sleep
            ft.TextField(
                label="Drop Sleep (seconds)",
                value=str(settings['drop_sleep'])
            ),

            # Drop message
            ft.TextField(
                label="Drop Message",
                value=settings['drop_message'],
                multiline=True
            ),

            # GIF keyword
            ft.TextField(
                label="GIF Keyword",
                value=settings['gif_keyword']
            ),

            # Checkboxes
            ft.Checkbox(label="Randomize GIF", value=settings['randomize']),
            ft.Checkbox(label="Skip Chudai", value=settings['skip_chudai']),
            # ... more checkboxes
        ]),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
            ft.TextButton("Save", on_click=lambda e: save_and_close(settings))
        ]
    )

    self.page.dialog = dialog
    dialog.open = True
    self.page.update()
```

**What It Does:**
- Shows popup dialog
- Input fields for all settings
- Save button updates `self.all_settings`

---

### 9. NETWORK OPERATIONS

#### A. License Linking

**Function:** `_link_license_remote(self, license_key)`
**Location:** Line ~120 in XBot_complete_source.py

**Logic That Goes Here:**
```python
async def _link_license_remote(self, license_key):
    async with httpx.AsyncClient() as client:
        # POST to link endpoint
        response = await client.post(
            f"{API_BASE}/clients/licenses/link",
            json={
                'client_id': CLIENT_ID,
                'license_key': license_key
            }
        )

        if response.status_code == 200:
            return True
        else:
            return False
```

**Network Call:**
```
POST /clients/licenses/link
Body: {"client_id": "uuid-here", "license_key": "XXXX"}
```

#### B. Restore Licenses

**Function:** `_restore_licenses(self)`
**Location:** Line ~453 in XBot_complete_source.py

**Logic That Goes Here:**
```python
async def _restore_licenses(self):
    async with httpx.AsyncClient() as client:
        # GET all licenses for this client
        response = await client.get(
            f"{API_BASE}/clients/{CLIENT_ID}/licenses"
        )

        if response.status_code == 200:
            data = response.json()
            licenses = data['licenses']

            # Restore each license
            for lic in licenses:
                self._add_license_to_data(
                    lic['key'],
                    lic['browser_id'],
                    lic['model'],
                    lic['expires'],
                    link_remote=False  # Already linked
                )

            # Save to disk
            self._save_profiles_local()
```

**What It Does:**
- Fetches licenses from server
- Restores them to local storage
- Used when switching devices

---

### 10. PAYMENT/PURCHASE UI

**Class:** `PurchaseUI`
**Location:** Separate class (referenced in XBot_complete_source.py)

**Logic Structure:**
```python
class PurchaseUI:
    def show_payment_dialog(self, license_type):
        # Show crypto selection
        # Options: BTC, ETH, XMR, etc.
        pass

    def generate_qr_code(self, address, amount):
        # Generate QR code URL
        url = f"https://quickchart.io/qr?text={address}"
        return url

    def check_payment_status(self, transaction_id):
        # Poll server for payment confirmation
        # Return True when paid
        pass
```

**What It Does:**
- Shows cryptocurrency payment UI
- Generates QR codes for wallet addresses
- Monitors payment status

---

## 🔄 Program Flow

### Startup Sequence
```
1. main(page, restore=False) called by Flet
   ↓
2. XBotApp.__init__(page)
   ↓
3. _load_profiles_local()
   ↓
4. _load_settings_local()
   ↓
5. _render_main_dashboard()
   ↓
6. [UI shows - waiting for user input]
```

### Running Bot Sequence
```
1. User clicks "Run" button on profile
   ↓
2. _toggle_run(pid) called
   ↓
3. asyncio.create_task(_run_automation(pid))
   ↓
4. _run_automation(pid) executes:
   - Launch browser
   - Login to Twitter
   - Loop: Send messages
   - Update UI each iteration
   ↓
5. When done: Update status, close browser
```

### Settings Change Sequence
```
1. User clicks "Settings" button
   ↓
2. _show_settings_dialog(pid)
   ↓
3. Dialog shows with current values
   ↓
4. User changes values, clicks Save
   ↓
5. Update self.all_settings
   ↓
6. _save_settings_local()
   ↓
7. New settings written to .settings.json
```

---

## 📊 Data Flow

### Where Data Lives

```
MEMORY:
├── self.accounts[]              ← Licenses + profiles
│   └── [{'key': 'XXX', 'profiles': [...]}]
│
├── self.all_settings{}          ← Bot configuration
│   └── {'drop_limit': 50, 'drop_sleep': 5, ...}
│
├── self.states{}                ← Runtime state per profile
│   └── {pid: {'paused': False, 'drop_count': 0, ...}}
│
└── self.page                    ← Flet UI reference

DISK:
├── .xbot_profiles.json          ← Persistent profiles
├── .settings.json               ← Persistent settings
└── System Keyring               ← Passwords

NETWORK:
└── API_BASE server              ← License validation
```

### Data Transformations

```
.xbot_profiles.json
    ↓ [_load_profiles_local()]
self.accounts[]
    ↓ [_license_card()]
UI License Cards
    ↓ [User clicks "Run"]
_run_automation(pid)
    ↓ [Browser automation]
Twitter DMs sent
```

---

## 🎯 Key Functions Summary

| Function | Purpose | Where Logic Goes |
|----------|---------|------------------|
| `__init__` | Initialize app | Set up data structures |
| `_load_profiles_local` | Load saved data | Read JSON, parse, populate arrays |
| `_save_profiles_local` | Save data | Convert to JSON, write file |
| `_check_license` | Validate license | HTTP GET to server |
| `_render_main_dashboard` | Show UI | Create Flet components |
| `_license_card` | Create license card | Build UI card widget |
| `_run_automation` | **CORE: Run bot** | Browser automation, spam loop |
| `_toggle_run` | Start/stop bot | Create/cancel async task |
| `_show_settings_dialog` | Settings UI | Show dialog, handle save |
| `_ensure_pid_state` | Track state | Create state dict if missing |

---

## 🔍 Finding Specific Logic

### "Where does it log into Twitter?"
→ `_run_automation()` calls helper method `_login_twitter()`
→ Happens at start of automation sequence

### "Where does it send spam messages?"
→ Inside `_run_automation()` main loop
→ Calls helper method `_send_dm()`

### "Where are passwords stored?"
→ System keyring via `keyring.get_password('XBot', 'XBot.py')`
→ Called in `_run_automation()` before browser launch

### "Where does it check license?"
→ `_check_license(key)` function
→ Called when: Adding license, restoring, before running

### "Where is UI rendered?"
→ `_render_main_dashboard()` - main screen
→ `_render_bootstrap()` - startup screen
→ `_license_card()` - individual cards

---

This map shows you **what goes where** without providing the actual malicious implementation. Perfect for understanding the architecture!
