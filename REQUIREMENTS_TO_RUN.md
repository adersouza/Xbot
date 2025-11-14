# What's Needed to Run XBot - Complete Requirements

This documents everything required to operate XBot for defensive understanding.

---

## 1. System Requirements

### Operating System
- **Windows 10/11** (64-bit)
- The .exe is Windows-specific (PyInstaller for Windows)

### Hardware
- 4GB+ RAM (for browser automation)
- 500MB+ free disk space
- Internet connection

---

## 2. Software Dependencies (Embedded in .exe)

The PyInstaller package includes:

```
python313.dll              # Python 3.13 runtime (5.8MB)
python3.dll               # Python stub

# Core libraries (all included):
├── playwright/           # Browser automation
├── keyring/             # Credential storage
├── aiohttp/             # Async HTTP
├── httpx/               # Modern HTTP client
├── flet/                # GUI framework
├── PIL/                 # Image processing
├── numpy/               # Data processing
├── psutil/              # System monitoring
├── pyyaml/              # Config parsing
├── certifi/             # SSL certificates
├── charset_normalizer/  # Encoding
├── greenlet/            # Concurrency
├── multidict/           # Data structures
├── propcache/           # Property caching
└── frozenlist/          # Immutable lists

# Windows runtime DLLs (all included):
├── VCRUNTIME140.dll
├── VCRUNTIME140_1.dll
├── ucrtbase.dll
├── libcrypto-3.dll      # 5MB - OpenSSL crypto
├── libssl-3.dll         # 774KB - SSL/TLS
└── api-ms-win-*.dll     # 40+ Windows API stubs
```

**Important**: User does NOT need to install Python or any libraries. Everything is bundled!

---

## 3. Browser Requirements

### Playwright Browser Installation

**First-time setup** (one-time only):

After running XBot.exe for the first time, user must run:

```cmd
# XBot will prompt or auto-run this:
playwright install chromium

# Or manually:
cd %TEMP%\_MEI<random>
playwright.exe install chromium
```

This downloads (~150MB):
- Chromium browser (~130MB)
- Browser dependencies
- WebDriver components

**Location**:
```
%USERPROFILE%\AppData\Local\ms-playwright\chromium-<version>\
```

**Why needed**: Playwright controls a real Chrome browser to interact with Twitter

---

## 4. Twitter Accounts (CRITICAL)

### Account Requirements

User needs **active Twitter accounts** to spam from:

```
Minimum: 1 account
Recommended: 5-10 accounts (for rotation)
Maximum: Unlimited

Account requirements:
✓ Active Twitter account (not suspended)
✓ Email verified
✓ Phone verified (recommended)
✓ Past rate limits threshold
✓ Has posted at least a few tweets (not brand new)
```

### Account Credentials Needed

For each account:
```
- Username/Handle: @example
- Email: account@email.com
- Password: account_password
- (Optional) 2FA backup codes
```

These are stored in:
```
.xbot_profiles.json - Profile metadata
Windows Credential Manager - Passwords (via keyring)
```

---

## 5. Target Lists (CRITICAL)

### What Are Targets?

Targets = Twitter users/groups to spam. The bot needs a list of who to message.

### How Targets Are Provided

**Option A: Manual Entry**
```
User manually enters Twitter handles:
- @user1
- @user2
- @user3
```

**Option B: Import from File**
```
targets.txt:
user1
user2
user3
```

**Option C: Group/Community Lists**
```
Twitter group IDs or community member lists
```

**Option D: Scraper Integration** (likely exists but we didn't see it)
```
Scrapes Twitter for:
- Users in specific niches
- Members of competitor groups
- Followers of specific accounts
- Users who posted with certain hashtags
```

### Target Data Structure

Each target needs:
```json
{
  "id": "123456789",
  "username": "target_user",
  "name": "Target User",
  "followers": 1000,
  "has_onlyfans_link": true
}
```

**Missing from decompilation**: We didn't see where targets come from. Possibilities:
1. Separate scraper tool
2. Manual CSV import
3. Built-in scraper (in parts we couldn't fully decompile)
4. Purchased target lists

---

## 6. License Key (In Legitimate Version)

### License System

**Legitimate version requires**:
- License key purchased from @PurchaseTwitterXBot
- Format: `XXXX-XXXX-XXXX-XXXX` (example)
- Validated against license server

**Pricing tiers** (from strings):
```
Base License:
- Single account
- Limited drops/day
- Basic features

Upgrade:
- Multiple accounts
- Higher drop limits
- Scheduling

Lifetime:
- Unlimited accounts
- Unlimited drops
- All features
- Priority support
```

**Payment methods**:
- Bitcoin (BTC)
- Ethereum (ETH)
- Monero (XMR)
- Other cryptocurrencies

**In cracked version**:
- License check bypassed
- All features unlocked
- Warning: "Please purchase from @PurchaseTwitterXBot on Telegram instead"

---

## 7. Configuration (User Must Set)

### Initial Setup

User must configure in GUI:

#### **Spam Settings**
```
drop_limit: 50           # How many messages to send
drop_sleep: 5            # Seconds between messages
rate_limit_sleep: 60     # Wait time when rate limited

drop_message:            # The spam message
"Hit my pinned post
Please add me to your groups"
```

#### **GIF Settings**
```
gif_keyword: "hello"     # Search term for GIFs
randomize: true          # Random GIF selection
no_gif: false            # Disable GIF attachment
```

#### **Evasion Settings**
```
skip_missing_followers: true
skip_chudai: true
leniency_1_3: true
leniency_1_4: true
leniency_2_5: true
```

#### **Skip List**
```
group_skip: []           # Groups/users to skip
```

---

## 8. Network/Firewall Requirements

### Outbound Connections Required

Bot needs to connect to:

```
1. Twitter.com
   - https://twitter.com/*
   - https://x.com/*
   - Login, messaging, API

2. Font Loading
   - https://rsms.me/inter/font-files/
   - For GUI fonts

3. QR Code Generation (for payments)
   - https://quickchart.io/qr?text=
   - Payment QR codes

4. License Server (legitimate version)
   - API_BASE endpoint (URL not in strings)
   - License validation
```

**Firewall rules**: Must allow outbound HTTPS on port 443

---

## 9. Disk Space Requirements

### Initial Installation
```
XBot.exe:                    ~50MB (compressed)
Extracted files:             ~35MB
  ├── Python runtime:        ~15MB
  ├── Libraries:             ~15MB
  └── Resources:             ~5MB
```

### Runtime
```
Playwright Chromium:         ~150MB
Browser cache:               ~50MB
Profile data:                ~5MB
Logs:                        ~10MB
```

**Total**: ~300MB disk space

**Location**:
```
%TEMP%\_MEI<random>\         # Temp extraction (auto-deleted on exit)
%APPDATA%\Local\ms-playwright\  # Browser (permanent)
.xbot_profiles.json          # Config (current directory)
.settings.json               # Settings (current directory)
```

---

## 10. Windows Permissions Required

### What Access Does It Need?

```
✓ File system: Read/Write in current directory
✓ Registry: Windows Credential Manager access
✓ Network: Outbound HTTPS connections
✓ Process: Spawn browser processes
✓ GUI: Create application window

✗ Does NOT require:
  - Administrator rights
  - System-level access
  - Driver installation
  - Kernel-mode access
```

**Runs as normal user** - No elevation required

---

## 11. First-Time Setup Flow

### What User Actually Does

1. **Download XBot.exe**
   - From Telegram seller (@PurchaseTwitterXBot)
   - Or cracked version from forums

2. **Run XBot.exe**
   - Double-click
   - Windows Defender may warn (unsigned .exe)
   - Extracts to %TEMP%\_MEI<random>\

3. **First Launch Prompt**
   ```
   "Welcome to XBOT"
   [Create New Identity] [Restore Identity]
   ```

4. **Install Playwright Browser** (if not already)
   ```
   > playwright install chromium
   Installing Chromium...
   ✓ Done
   ```

5. **Add Twitter Account**
   ```
   Username: @myaccount
   Email: myemail@gmail.com
   Password: ********
   License Key: XXXX-XXXX-XXXX (optional in cracked version)
   [Add Profile]
   ```

6. **Configure Settings**
   ```
   Drop Limit: [slider: 50]
   Drop Sleep: [slider: 5s]
   Message: [text box: "Hit my pinned post..."]
   GIF Keyword: [text: "hello"]
   [Save Settings]
   ```

7. **Add Targets** (MISSING - unclear how in our analysis)
   - Import CSV?
   - Manual entry?
   - Built-in scraper?

8. **Click "Run"**
   - Browser opens
   - Logs into Twitter
   - Starts sending spam

---

## 12. Optional/Advanced Features

### Scheduling
```
Schedule bot to run at specific time:
- Start time: 2:00 AM
- Runs automatically when time reached
```

### Profile Presets
```
Save/load different configurations:
- "Aggressive" - High volume, short delays
- "Stealth" - Low volume, long delays
- "Default" - Balanced
```

### Multiple Accounts
```
Add multiple Twitter accounts
Run simultaneously or rotate
```

---

## 13. What's MISSING (That We Couldn't Find)

### Target Acquisition

**Big question**: How do users get target lists?

Possibilities:
1. **Separate scraper tool** - Not in this .exe
2. **Manual CSV import** - Likely exists but not seen
3. **Built-in scraper** - May be in parts that failed to decompile
4. **Purchased lists** - Buy from seller
5. **API integration** - Connects to external service

**This is critical** - Without targets, bot can't run!

### Proxy Support

Didn't see proxy configuration in strings. Questions:
- Can it use proxies?
- Built-in proxy rotation?
- SOCKS5 support?

### Anti-Detection

Saw some evasion flags but unclear:
- What do leniency_1_3, leniency_1_4, leniency_2_5 actually do?
- Are there more advanced evasion techniques?
- Browser fingerprint randomization?

---

## 14. Complete Checklist

### What User MUST Have:

✅ **Hardware**
- Windows PC
- 4GB+ RAM
- Internet connection

✅ **Accounts**
- 1+ Twitter accounts (verified)
- Account credentials

✅ **Targets**
- List of users to message
- (How obtained is unclear)

✅ **Configuration**
- Spam message text
- Drop limits and timing
- GIF settings

✅ **Software** (auto-installed)
- XBot.exe (provided)
- Playwright Chromium (auto-installed)

✅ **Optional**
- License key (bypassed in crack)
- Multiple accounts for rotation

---

## 15. Red Flags for Detection

### On User's System

If you find these, XBot is installed:

```
Files:
✓ XBot.exe (anywhere)
✓ .xbot_profiles.json (contains Twitter credentials!)
✓ .settings.json (contains spam configuration)
✓ %TEMP%\_MEI* directories
✓ %APPDATA%\Local\ms-playwright\chromium-*

Processes:
✓ XBot.exe
✓ python.exe (as child of XBot.exe)
✓ chromium.exe or chrome.exe (as child)
✓ playwright.exe

Registry:
✓ Windows Credential Manager entries:
   Service: "XBot"
   Usernames: "client_*"

Network:
✓ Repeated connections to twitter.com
✓ Regular timing patterns
✓ Multiple DM sends in short time
```

---

## Summary: Complete Requirements

| Requirement | Status | Source |
|------------|--------|--------|
| Windows OS | Required | PE format |
| Python 3.13 | Bundled | Included in .exe |
| Playwright | Bundled + Browser | Auto-installed |
| Twitter accounts | REQUIRED | User provides |
| Account credentials | REQUIRED | User provides |
| Target lists | REQUIRED | **Unclear source** |
| License key | Optional | Bypassed in crack |
| Spam message | Required | User configures |
| Drop settings | Required | User configures |
| GIF keyword | Optional | User configures |
| 300MB disk space | Required | System |
| Network access | Required | Firewall |

**Critical Missing Piece**: **Target acquisition method is unclear**

This is the biggest unknown - without knowing how users get target lists, we're missing a key component. It's likely:
- Separate tool/script
- External service
- Manual import
- Built-in scraper that failed to decompile

---

**For defenders**: Monitor for the file/process/network indicators above. The credentials in `.xbot_profiles.json` are especially valuable for incident response.
