# XBot Deployment Process - Threat Intelligence Analysis

**Document Purpose:** Educational analysis for defensive security research, incident response, and threat intelligence. This documents how threat actors deploy XBot to help defenders understand the attack chain, detect deployment artifacts, and identify compromise indicators.

**⚠️ WARNING:** This document describes malware deployment for defensive analysis only. Operating spam bots violates Twitter Terms of Service and may violate computer fraud laws. This analysis is for security professionals, researchers, and defenders.

---

## Table of Contents

1. [Adversary Setup Overview](#adversary-setup-overview)
2. [Pre-Deployment Requirements](#pre-deployment-requirements)
3. [Initial Deployment Steps](#initial-deployment-steps)
4. [Configuration Process](#configuration-process)
5. [Operational Execution](#operational-execution)
6. [Detection Opportunities](#detection-opportunities)
7. [Defensive Countermeasures](#defensive-countermeasures)

---

## Adversary Setup Overview

### Deployment Chain

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: Acquisition                                            │
├─────────────────────────────────────────────────────────────────┤
│ Attacker obtains XBot.exe (cracked version)                     │
│ Sources: Telegram channels, forums, file sharing                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: Infrastructure Setup                                   │
├─────────────────────────────────────────────────────────────────┤
│ - Windows machine (VM or physical)                              │
│ - Twitter accounts (purchased or created)                       │
│ - Target lists (scraped or purchased)                           │
│ - Optional: Proxies, VPN                                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: Initial Execution                                      │
├─────────────────────────────────────────────────────────────────┤
│ - Run XBot.exe (bypassed license check)                         │
│ - Install Playwright browser                                    │
│ - Create identity (CLIENT_ID + PASSWORD)                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: Configuration                                          │
├─────────────────────────────────────────────────────────────────┤
│ - Add Twitter account profiles                                  │
│ - Configure spam message and settings                           │
│ - Load target lists                                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: Execution                                              │
├─────────────────────────────────────────────────────────────────┤
│ - Launch automation                                             │
│ - Bot posts spam messages via Playwright                        │
│ - Continues until drop_limit reached                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pre-Deployment Requirements

### What Attackers Need Before Starting

#### 1. Windows Environment

**Minimum System:**
```
OS: Windows 10 or Windows 11 (64-bit)
RAM: 4GB minimum (8GB recommended)
Disk: 1GB free space
Network: Stable internet connection
```

**Common deployment environments:**
- Personal Windows PC (risky - direct attribution)
- Windows VPS (Vultr, DigitalOcean) - common choice
- Azure/AWS Windows VM (more expensive)
- Residential proxy + local machine
- Hacked/compromised Windows machines (advanced)

#### 2. Twitter Accounts

**Account acquisition methods observed:**

**Method A: Self-created accounts**
```
- Create 5-10 Twitter accounts
- Use different email providers (Gmail, Outlook, ProtonMail)
- Phone verify with VOIP numbers or SMS services
- Age accounts for 1-2 weeks before use
- Post some legitimate tweets (avoid new account flags)
```

**Method B: Purchased accounts**
```
Sources:
- Underground forums (Nulled, BlackHatWorld)
- Telegram channels
- Account shops (accsmarket, etc.)

Pricing observed:
- Aged account (6+ months): $2-5 each
- Phone verified: $1-3 each
- Email verified only: $0.50-1 each
- Bulk discounts: 100 accounts for $100-200
```

**Method C: Hacked/compromised accounts**
```
- Credential stuffing attacks
- Phishing campaigns
- Database breaches
- Less common for spam (easier to just buy)
```

**Account requirements:**
```
✓ Email verified
✓ Phone verified (preferred)
✓ Not suspended/locked
✓ Past new account restrictions
✓ Some tweet history (looks more legitimate)
```

#### 3. Target Lists

**How attackers obtain targets:**

**Method A: Twitter scraping tools**
```
Common tools:
- Twint (Twitter scraper)
- TweetScraper
- Custom Selenium/Playwright scrapers
- Commercial scraping APIs

Targeting criteria:
- Users in specific niches (crypto, OF creators, etc.)
- Followers of competitor accounts
- Members of Twitter communities
- Users posting specific hashtags
- Bio contains keywords ("OnlyFans", "Fansly", etc.)
```

**Method B: Purchased target lists**
```
Sources:
- Telegram channels selling data
- Underground forums
- Data brokers

Example pricing:
- 10,000 targeted profiles: $50-100
- 100,000 generic profiles: $200-500
- Niche-specific (OF creators): Premium pricing
```

**Method C: Manual compilation**
```
- Manually browse Twitter
- Copy usernames to text file
- Small scale but free
```

---

## Initial Deployment Steps

### Step 1: Obtain XBot.exe (Cracked Version)

**Attacker acquisition process:**

```
Common distribution channels:
1. Telegram: "Free tools" channels, cracking groups
2. Forums: Nulled.to, BlackHatWorld, MPGH
3. File sharing: MEGA.nz, MediaFire, AnonFiles
4. GitHub/GitLab: Occasionally uploaded by crackers or researchers
```

**File verification (attackers check):**
```powershell
# Check file size (should be ~9-10MB)
Get-Item XBot.exe | Select-Object Length

# Some check hash against known good cracks
Get-FileHash XBot.exe -Algorithm SHA256
```

**Security note:** Attackers downloading cracked tools face risk of backdoored versions (ironic - criminals getting scammed by other criminals).

---

### Step 2: Initial Execution

**First run process:**

#### 2a. Launch XBot.exe

```powershell
# Typical execution (double-click or command line)
.\XBot.exe

# Some run in background
Start-Process XBot.exe -WindowStyle Hidden
```

**What happens on first launch:**
```
1. PyInstaller unpacks to %TEMP%\_MEI<random>\
2. Flet GUI window appears
3. Bootstrap screen shows (if first run)
4. License check executes (bypassed - always returns True)
```

**Filesystem artifacts created:**
```
%TEMP%\_MEI<random>\                    # PyInstaller temp extraction
%APPDATA%\Local\ms-playwright\          # Browser install location (after step 2b)
%USERPROFILE%\.xbot_profiles.json       # Profile config (after step 3)
```

#### 2b. Install Playwright Browser (Critical Step)

**The problem:** XBot requires Playwright Chromium browser, which is NOT bundled in the .exe.

**Attacker must manually install:**

```powershell
# Error on first run if not installed:
# "playwright._impl._api_types.Error: Executable doesn't exist at ..."

# Installation methods:

# Method A: If playwright.exe is in PATH (rare with PyInstaller)
playwright install chromium

# Method B: Find embedded playwright and run (more common)
# After XBot.exe runs once, it extracts to temp directory
cd %TEMP%\_MEI<random>\playwright\driver\
playwright.exe install chromium

# Method C: Install Python and playwright globally (overcomplicated)
pip install playwright
playwright install chromium
```

**What this downloads:**
```
Chromium browser: ~130MB
Location: %USERPROFILE%\AppData\Local\ms-playwright\chromium-<version>\

Files:
- chrome.exe (the browser)
- chrome_100_percent.pak
- chrome_200_percent.pak
- icudtl.dat
- locales\ (language files)
- resources.pak
- v8_context_snapshot.bin
```

**Detection opportunity:** Monitor for `playwright install` commands and Chromium downloads to unusual locations.

---

### Step 3: Bootstrap - Create Identity

**First-time setup screen:**

When XBot launches (and no existing identity found), Bootstrap screen appears:

**Option A: Create New Identity**

```
User enters:
├── CLIENT_ID: "user_chosen_id"          # Any string (e.g., "john_xbot_2024")
└── PASSWORD: "user_chosen_password"     # Any string (e.g., "MySecurePass123")

XBot stores:
├── CLIENT_ID → .xbot_profiles.json
└── PASSWORD → Windows Credential Manager
    Service: "XBot"
    Account: CLIENT_ID
    Password: PASSWORD
```

**Storage locations:**
```
Profile metadata:
└── %USERPROFILE%\.xbot_profiles.json

Credential storage:
└── Windows Credential Manager
    Path: Control Panel > Credential Manager > Windows Credentials
    Entry: "XBot:user_chosen_id"
```

**Option B: Restore Existing Identity**

```
User enters same CLIENT_ID + PASSWORD used previously
XBot validates against Windows Credential Manager
If match: loads existing profiles from .xbot_profiles.json
If no match: shows error
```

**Detection opportunity:** Monitor for `.xbot_profiles.json` file creation and "XBot" entries in Credential Manager.

---

## Configuration Process

### Step 4: Add Twitter Account Profiles

**After bootstrap, main dashboard appears:**

#### Adding a Profile

**GUI workflow:**

```
1. Click "Add Profile" button
2. Dialog appears with fields:
   ├── Email: twitter_account@email.com
   ├── Username: @twitter_handle
   └── Password: twitter_password
3. Click "Submit"
```

**Backend storage process:**

```python
# What XBot does when profile added:

# 1. Generate unique profile ID
profile_id = str(uuid.uuid4())  # e.g., "a3f4c2d1-..."

# 2. Store profile metadata in JSON
profile_data = {
    "id": profile_id,
    "email": email,
    "username": username,
    "client_id": CLIENT_ID  # Links to identity
}

# Save to .xbot_profiles.json:
{
    "profiles": [
        {
            "id": "a3f4c2d1-...",
            "email": "account1@email.com",
            "username": "@account1",
            "client_id": "user_chosen_id"
        },
        {
            "id": "b7e9f3a2-...",
            "email": "account2@email.com",
            "username": "@account2",
            "client_id": "user_chosen_id"
        }
    ]
}

# 3. Store password in Credential Manager
keyring.set_password(
    service="XBot",
    username=CLIENT_ID,  # Links to identity
    password=twitter_password
)
```

**Attacker typically adds 5-10 accounts for rotation.**

**Detection opportunity:**
- Multiple Twitter login attempts from same IP/machine
- `.xbot_profiles.json` file monitoring
- Credential Manager "XBot" entries

---

### Step 5: Configure Settings

**Settings dialog configuration:**

```
Spam Message Settings:
├── drop_limit: 50                # Stop after 50 messages
├── drop_sleep: 5                 # Wait 5 seconds between messages
├── rate_limit_sleep: 60          # Wait 60 seconds if rate limited
├── randomize: true               # Add random variance to timing
└── drop_message:                 # The spam message
    "Hit my pinned post
    Please add me to your groups"

GIF Settings:
├── attach_gif: true
├── gif_keyword: "funny"          # Search keyword for GIF
└── gif_selector: 0               # Which GIF from search results

Evasion Settings:
├── skip_missing_followers: true  # Skip targets with no followers
├── skip_verified: false          # Don't skip verified accounts
└── has_onlyfans_link: true       # Only target users with OF links in bio

Account Settings:
└── multiple profiles added       # List of Twitter accounts
```

**These settings are stored in `.xbot_profiles.json` or separate config file.**

---

### Step 6: Load Target Lists

**The critical missing component:**

Attackers need to load a list of Twitter users to spam. Based on analysis, this likely works via:

**Method A: Manual input**
```
GUI has text area
User pastes usernames:
@user1
@user2
@user3
```

**Method B: File import**
```
targets.txt:
user1
user2
user3

OR

targets.csv:
username,followers,has_of_link
user1,1000,true
user2,500,false

XBot imports this file
```

**Method C: Integrated scraper** (most likely but not found in decompilation)
```
User enters scraping criteria:
├── Hashtag: #crypto
├── Limit: 1000
└── Min followers: 100

XBot scrapes Twitter and builds target list
```

**Method D: External tool**
```
Separate XBot_Scraper.exe (if exists)
Exports targets.json
XBot.exe imports this file
```

**Detection opportunity:**
- Large text files with Twitter usernames
- CSV files with user data
- Scraping tools running alongside XBot
- Network traffic to Twitter search/API endpoints

---

## Operational Execution

### Step 7: Launch Automation

**Starting the bot:**

```
1. User selects a profile from dashboard
2. Clicks "Run" button next to profile
3. XBot launches automation:

Execution flow:
├── 1. Launch Playwright browser (headless or visible)
├── 2. Navigate to twitter.com/i/flow/login
├── 3. Enter email/username
├── 4. Enter password (from Credential Manager)
├── 5. Handle 2FA if enabled (manual or automated)
├── 6. Wait for successful login
├── 7. Begin spam loop:
│   ├── For each target in list:
│   │   ├── Navigate to target's profile/DMs
│   │   ├── Check if should skip (filters)
│   │   ├── Post spam message
│   │   ├── Attach GIF (optional)
│   │   ├── Click send
│   │   ├── Increment drop counter
│   │   ├── Sleep for drop_sleep seconds (+ randomization)
│   │   ├── Check if rate limited (handle if yes)
│   │   └── Check if drop_limit reached (stop if yes)
│   └── End loop
└── 8. Display completion status
```

**GUI status updates during execution:**

```
Profile row shows:
├── Status: "Running..." → "Completed" / "Rate Limited" / "Error"
├── Progress: "Drops: 23/50"
├── Timer: "Running for: 00:05:32"
└── Controls: "Stop" button enabled
```

---

### Step 8: Monitoring and Adjustments

**Attacker monitors execution:**

**Success indicators:**
```
✓ Messages sent successfully
✓ No rate limit warnings
✓ Accounts not suspended
✓ Drop counter incrementing
```

**Failure indicators:**
```
✗ "Rate limited" status
✗ Account suspended notification
✗ Login failures
✗ Browser automation detected
✗ Error messages
```

**Adjustments attackers make:**

```
If rate limited:
├── Increase drop_sleep (slow down)
├── Switch to different account
└── Wait before resuming

If detected/suspended:
├── Add more randomization
├── Use residential proxies
├── Age accounts longer before use
└── Reduce drop_limit (be less aggressive)

If targets not responding:
├── Change target selection criteria
├── Update spam message
└── Try different niche
```

---

### Step 9: Rotation and Scaling

**Multi-account rotation:**

```
Strategy 1: Sequential rotation
├── Account 1: 50 drops → stop
├── Wait 1 hour
├── Account 2: 50 drops → stop
├── Wait 1 hour
└── Repeat cycle

Strategy 2: Concurrent rotation
├── Account 1: 10 drops → pause
├── Account 2: 10 drops → pause
├── Account 3: 10 drops → pause
└── Return to Account 1, repeat

Strategy 3: Scheduled execution
├── Account 1: Run at 9am
├── Account 2: Run at 12pm
├── Account 3: Run at 3pm
└── Account 4: Run at 6pm
```

**Scaling operations:**

```
Small scale (1 operator):
├── 1 Windows machine
├── 5-10 Twitter accounts
├── 250-500 messages/day
└── Manual monitoring

Medium scale (organized):
├── 3-5 Windows VPS instances
├── 50-100 Twitter accounts
├── 2,500-5,000 messages/day
└── Semi-automated monitoring

Large scale (operation):
├── 20+ Windows VPS instances
├── 500+ Twitter accounts
├── 25,000+ messages/day
└── Fully automated with monitoring dashboard
```

---

## Detection Opportunities

### Deployment Phase Detection

**Phase 1: File acquisition**
```
Indicators:
├── XBot.exe downloaded from suspicious sources
├── File hash matches known malware
├── VirusTotal submissions
└── Network logs showing file-sharing sites
```

**Phase 2: Initial execution**
```
Indicators:
├── PyInstaller extraction to %TEMP%\_MEI*
├── playwright.exe execution
├── Chromium download to AppData\Local\ms-playwright\
├── New process: chrome.exe with automation flags
└── Network: playwright CDN connections
```

**Phase 3: Configuration**
```
Indicators:
├── .xbot_profiles.json file creation
├── Windows Credential Manager entries (service: "XBot")
├── Multiple JSON writes to profile file
└── Filesystem monitoring alerts
```

---

### Operational Phase Detection

**Network indicators:**
```
├── Repeated connections to twitter.com
├── Browser automation user-agent strings
├── High frequency API/web requests
├── Pattern: login → action → logout → login (cycling accounts)
└── Connections to playwright CDN (if downloading browser)
```

**Behavioral indicators:**
```
├── Identical messages sent from multiple accounts
├── Consistent timing between messages (drop_sleep)
├── Same GIF attached repeatedly
├── Messages match known spam patterns
└── Accounts created in batches, used together
```

**Filesystem indicators:**
```
├── .xbot_profiles.json exists
├── Chromium in ms-playwright directory (without legitimate Playwright dev work)
├── Windows Credential Manager entries for "XBot"
└── Large target list files (CSV/TXT with Twitter usernames)
```

**Process indicators:**
```
├── XBot.exe running (process name)
├── chrome.exe with flags: --enable-automation, --remote-debugging-port
├── python313.dll loaded in memory
└── Playwright-related DLLs
```

---

## Defensive Countermeasures

### For Endpoint Security (IT/SOC Teams)

**Detection rules:**

```yaml
# YARA rule for XBot detection
rule XBot_Spam_Bot {
    meta:
        description = "Detects XBot Twitter spam bot"
        author = "Security Researcher"
        date = "2024-11-14"

    strings:
        $s1 = "XBot V2.1" ascii wide
        $s2 = "@PurchaseTwitterXBot" ascii wide
        $s3 = "Please purchase from @PurchaseTwitterXBot" ascii
        $s4 = ".xbot_profiles.json" ascii
        $s5 = "drop_limit" ascii
        $s6 = "drop_sleep" ascii
        $s7 = "playwright" ascii
        $s8 = "Hit my pinned post" ascii

    condition:
        uint16(0) == 0x5A4D and  // PE file
        4 of ($s*)
}
```

**Endpoint monitoring:**

```powershell
# Monitor for XBot artifacts
Get-ChildItem -Path $env:USERPROFILE -Filter ".xbot_profiles.json" -Recurse
Get-ChildItem -Path "$env:LOCALAPPDATA\ms-playwright" -ErrorAction SilentlyContinue

# Check Credential Manager for XBot entries
cmdkey /list | Select-String "XBot"

# Monitor for playwright installations
Get-EventLog -LogName Security -Source "Microsoft-Windows-PowerShell" |
    Where-Object {$_.Message -like "*playwright install*"}
```

**Prevention:**

```
1. Application whitelisting (block XBot.exe)
2. Disable PyInstaller executables (if not needed in environment)
3. Monitor Credential Manager writes
4. Alert on .json file creation in user home directories
5. Block playwright CDN downloads (if not legitimate use)
```

---

### For Platform Defenders (Twitter Security)

**Account-level detection:**

```python
# Pseudocode for Twitter's detection systems

def detect_xbot_spam(account):
    """Detect XBot automation patterns"""

    signals = []

    # Message patterns
    if account.recent_messages_identical(threshold=0.9):
        signals.append("identical_messages")

    # Timing patterns
    message_intervals = account.get_message_intervals(last_n=50)
    if is_constant_interval(message_intervals, variance=0.2):
        signals.append("constant_timing")  # drop_sleep pattern

    # Browser automation
    if account.user_agent.contains("HeadlessChrome") or \
       account.user_agent.contains("playwright"):
        signals.append("automation_detected")

    # Content patterns
    if account.message_contains("Hit my pinned post"):
        signals.append("known_spam_message")

    # Attachment patterns
    if account.messages_have_same_gif(threshold=0.8):
        signals.append("repeated_gif")

    # Account age vs activity
    if account.age_days < 30 and account.message_count > 100:
        signals.append("new_account_high_activity")

    # Calculate risk score
    risk_score = len(signals) * 10

    if risk_score > 30:
        take_action(account, signals)

def take_action(account, signals):
    """Take enforcement action"""
    if "automation_detected" in signals:
        account.suspend(reason="Automation")
    elif len(signals) >= 3:
        account.rate_limit(duration_hours=24)
    else:
        account.flag_for_review()
```

**Network-level detection:**

```
Monitor for:
├── Multiple accounts from same IP
├── Accounts cycling through shared IPs (rotation)
├── Browser fingerprint reuse across accounts
├── TLS fingerprint indicating Playwright/automation
└── Timing correlations across accounts
```

**Content-level detection:**

```
├── Regex matching known spam messages
├── GIF hash matching (same GIF attached repeatedly)
├── Link analysis (all accounts promoting same content)
└── NLP similarity detection (variations of same spam message)
```

---

### For Individual Users (Potential Targets)

**Protect yourself from XBot spam:**

```
1. Enable DM filtering (Settings > Privacy > Direct Messages)
   └── "Allow message requests from everyone" → OFF

2. Restrict who can message you
   └── "Only people you follow" → ON

3. Report spam immediately
   └── Report button → "Spam" → "Spam"

4. Block suspicious accounts
   └── Indicators: New account, no followers, generic name

5. Don't click links in unsolicited DMs
   └── Especially crypto/OF promotion links
```

---

## Conclusion

### Attack Chain Summary

```
Acquisition → Setup → Deployment → Configuration → Execution
    ↓           ↓         ↓             ↓              ↓
 Download    Windows   Run exe      Add accounts   Send spam
   .exe      +Twitter  +Install     +Configure     to targets
            accounts   Playwright    settings
```

### Critical Detection Points

**Highest value detection opportunities:**

1. **Playwright installation** - Very few legitimate users install Playwright
2. **`.xbot_profiles.json`** - Unique filename, easy to detect
3. **Credential Manager entries** - "XBot" service name is a dead giveaway
4. **Message timing patterns** - Constant intervals are non-human
5. **Identical messages** - Same text across accounts is obvious spam

### Defensive Priorities

**For Enterprises:**
1. Monitor for `.xbot_profiles.json` file creation
2. Alert on Playwright installations
3. Block known XBot.exe hashes
4. Monitor Windows Credential Manager writes

**For Twitter:**
1. Detect browser automation (user-agent, fingerprints)
2. Flag constant message timing patterns
3. Match known spam message signatures
4. Correlate accounts from same infrastructure

**For Users:**
1. Enable DM filtering
2. Report spam immediately
3. Don't engage with suspicious DMs

---

## Legal and Ethical Notice

**Using XBot is illegal and unethical:**

- ✗ Violates Twitter Terms of Service (account suspension)
- ✗ Violates Computer Fraud and Abuse Act (US)
- ✗ Violates equivalent laws in other jurisdictions
- ✗ Constitutes harassment/spam (civil liability)
- ✗ Undermines platform integrity
- ✗ Harms innocent users

**This document is for:**
- ✓ Security researchers analyzing threats
- ✓ Incident responders investigating incidents
- ✓ Platform defenders building detection
- ✓ Threat intelligence teams tracking adversaries
- ✓ Educational purposes (understanding attack chains)

**Do not use this information to:**
- ✗ Deploy XBot or similar tools
- ✗ Send spam on any platform
- ✗ Harass users
- ✗ Violate terms of service

---

## References

- XBOT_MALWARE_ANALYSIS.md - Technical capability analysis
- REQUIREMENTS_TO_RUN.md - Complete requirements documentation
- LICENSE_CRACK_ANALYSIS.md - License bypass analysis
- MISSING_COMPONENTS.md - Gap analysis
- extract_iocs.py - IOC extraction and YARA rules

**Document prepared for defensive security research - 2024-11-14**
