#!/usr/bin/env python3
"""
How to Discover Missing Logic from Bytecode
Educational guide on reverse engineering techniques
"""

import dis
import marshal


def demonstrate_bytecode_analysis():
    """
    Show how bytecode reveals control flow
    """
    print("="*80)
    print("METHOD 1: BYTECODE DISASSEMBLY")
    print("="*80)
    print()

    # Example function
    def example_function(x, limit):
        total = 0
        for i in range(limit):
            if x > 10:
                total += i * 2
            else:
                total += i
        return total

    print("SOURCE CODE:")
    print("-" * 40)
    print("""
def example_function(x, limit):
    total = 0
    for i in range(limit):
        if x > 10:
            total += i * 2
        else:
            total += i
    return total
""")

    print("\nBYTECODE DISASSEMBLY:")
    print("-" * 40)
    dis.dis(example_function)

    print("\n" + "="*80)
    print("WHAT BYTECODE TELLS US:")
    print("="*80)
    print("""
From the opcodes above, we can see:

1. CONTROL FLOW:
   - FOR_ITER instruction → Shows there's a loop
   - COMPARE_OP → Shows there's an if condition
   - POP_JUMP_IF_FALSE → Shows conditional branching
   - JUMP_BACKWARD → Shows loop repetition

2. OPERATIONS:
   - BINARY_OP (multiply) → Shows i * 2 calculation
   - BINARY_OP (add) → Shows += operations
   - COMPARE_OP (>) → Shows x > 10 comparison

3. STRUCTURE:
   - Instruction order → Shows execution sequence
   - Jump targets → Shows where branches go
   - Loop boundaries → Shows loop start/end
""")


def show_pattern_matching():
    """
    Show how to recognize common patterns
    """
    print("\n\n" + "="*80)
    print("METHOD 2: PATTERN RECOGNITION")
    print("="*80)
    print()

    print("Common bytecode patterns reveal logic:")
    print()

    print("PATTERN 1: Loop Structure")
    print("-" * 40)
    print("""
Bytecode sequence:
    LOAD_FAST (variable)
    GET_ITER
  → FOR_ITER (target)
    [loop body instructions]
    JUMP_BACKWARD
  → (target): continue after loop

Interpretation: for variable in iterable:
""")

    print("PATTERN 2: Conditional Statement")
    print("-" * 40)
    print("""
Bytecode sequence:
    LOAD_FAST (x)
    LOAD_CONST (10)
    COMPARE_OP (>)
    POP_JUMP_IF_FALSE (else_block)
    [if-true instructions]
    JUMP_FORWARD (after_if)
  → else_block:
    [if-false instructions]
  → after_if:

Interpretation: if x > 10: ... else: ...
""")

    print("PATTERN 3: Try/Except")
    print("-" * 40)
    print("""
Bytecode sequence:
    SETUP_EXCEPT (except_handler)
    [try body instructions]
    POP_BLOCK
    JUMP_FORWARD (after_except)
  → except_handler:
    [exception handling]
  → after_except:

Interpretation: try: ... except: ...
""")


def show_dynamic_analysis():
    """
    Show dynamic analysis techniques
    """
    print("\n\n" + "="*80)
    print("METHOD 3: DYNAMIC ANALYSIS (Run & Observe)")
    print("="*80)
    print()

    print("Technique 1: Tracing Execution")
    print("-" * 40)
    print("""
import sys

def trace_function(frame, event, arg):
    if event == 'line':
        # Capture: What line is executing
        print(f"Line {frame.f_lineno}: {frame.f_code.co_name}")

    elif event == 'call':
        # Capture: What function is called
        # Capture: What arguments are passed
        print(f"Call: {frame.f_code.co_name}({frame.f_locals})")

    elif event == 'return':
        # Capture: What value is returned
        print(f"Return: {arg}")

    return trace_function

sys.settrace(trace_function)
exec(bytecode)  # Now every operation is logged!
""")

    print("\nTechnique 2: Variable Watching")
    print("-" * 40)
    print("""
def watch_variables(frame, event, arg):
    # Capture variable values at each step
    if 'total' in frame.f_locals:
        print(f"total = {frame.f_locals['total']}")
    if 'i' in frame.f_locals:
        print(f"i = {frame.f_locals['i']}")
    return watch_variables

# Now we can see:
# - How variables change over time
# - What conditions trigger branches
# - Loop iteration counts
""")

    print("\nTechnique 3: Network/File Monitoring")
    print("-" * 40)
    print("""
# Monitor system calls
import strace  # Linux
strace -e trace=network python3 malware.pyc

# Captures:
# - Every HTTP request (URL, headers, body)
# - Every file read/write (path, content)
# - Every system call

# Or use monkey patching:
import httpx
original_get = httpx.AsyncClient.get

async def logged_get(self, url, **kwargs):
    print(f"HTTP GET: {url}")  # Log the call
    return await original_get(self, url, **kwargs)

httpx.AsyncClient.get = logged_get
""")


def show_comparative_analysis():
    """
    Show how comparing similar code helps
    """
    print("\n\n" + "="*80)
    print("METHOD 4: COMPARATIVE ANALYSIS")
    print("="*80)
    print()

    print("Compare against known implementations:")
    print()

    print("Step 1: Identify the libraries used")
    print("-" * 40)
    print("""
From bytecode we know XBot uses:
- playwright (browser automation)
- httpx (HTTP client)
- flet (GUI framework)
""")

    print("\nStep 2: Look at library documentation")
    print("-" * 40)
    print("""
Playwright documentation shows standard patterns:

# Login pattern
await page.goto('https://site.com/login')
await page.fill('input[name="username"]', username)
await page.fill('input[name="password"]', password)
await page.click('button[type="submit"]')

Since XBot has:
- Variables: page, username, password
- Function: _login_twitter
- Strings: 'https://twitter.com/login'

We can infer it likely uses this standard pattern!
""")

    print("\nStep 3: Study similar malware")
    print("-" * 40)
    print("""
Look at other Twitter bots:
- How do THEY select targets?
- What rate limiting do THEY use?
- What detection evasion do THEY implement?

Common patterns:
- Get followers list → Parse usernames → Filter
- Random delays between actions
- User-agent spoofing
- Cookie management
""")


def show_decompiler_comparison():
    """
    Show how multiple decompilers reveal different info
    """
    print("\n\n" + "="*80)
    print("METHOD 5: MULTIPLE DECOMPILER COMPARISON")
    print("="*80)
    print()

    print("Each decompiler has strengths:")
    print()

    print("pycdc (Best for structure):")
    print("-" * 40)
    print("""
- Shows: Function calls clearly
- Shows: Import statements
- Shows: Class structure
- Weakness: Fails on complex control flow
""")

    print("\nuncompyle6 (Best for older Python):")
    print("-" * 40)
    print("""
- Shows: Control flow well
- Shows: List comprehensions
- Shows: Exception handling
- Weakness: Doesn't support Python 3.13
""")

    print("\nManual disassembly (Always works):")
    print("-" * 40)
    print("""
import dis
dis.dis(code_object)

- Shows: Raw bytecode instructions
- Shows: Jump targets clearly
- Shows: Exact operation sequence
- Weakness: Requires manual interpretation
""")


def show_reverse_engineering_workflow():
    """
    Show the complete workflow
    """
    print("\n\n" + "="*80)
    print("COMPLETE REVERSE ENGINEERING WORKFLOW")
    print("="*80)
    print()

    print("""
PHASE 1: STATIC ANALYSIS (No execution)
----------------------------------------
1. Extract bytecode structure
   ✓ Function signatures
   ✓ String constants
   ✓ Variable names

2. Disassemble bytecode
   → Identify control flow patterns
   → Map function call graph
   → Identify algorithms used

3. Pattern matching
   → Compare against known patterns
   → Recognize standard libraries
   → Identify common techniques

Result: 30-40% understanding


PHASE 2: CONTROLLED EXECUTION (Sandbox)
----------------------------------------
4. Set up isolated VM
   → Network monitoring (Wireshark)
   → File monitoring (Process Monitor)
   → System call tracing

5. Instrument the code
   → Add sys.settrace()
   → Monkey patch key functions
   → Log all operations

6. Run and observe
   → Capture all network traffic
   → Log all function calls
   → Record variable values

Result: 70-80% understanding


PHASE 3: INTERACTIVE DEBUGGING
----------------------------------------
7. Use Python debugger (pdb)
   → Set breakpoints
   → Step through execution
   → Inspect variables

8. Modify and re-run
   → Change variables
   → Test hypotheses
   → Confirm behavior

Result: 90-95% understanding


PHASE 4: RECONSTRUCTION
----------------------------------------
9. Document findings
   → Write pseudocode
   → Create flowcharts
   → Map data flows

10. Implement clean version
    → Rewrite based on understanding
    → Test against original
    → Validate behavior matches

Result: 95-100% understanding
""")


def show_xbot_specific_example():
    """
    Show how this would work for XBot specifically
    """
    print("\n\n" + "="*80)
    print("APPLYING THIS TO XBOT")
    print("="*80)
    print()

    print("Question: How does _run_automation work?")
    print("-" * 40)
    print()

    print("STEP 1: Bytecode Analysis")
    print("""
From disassembly:
  LOAD_FAST (self)
  LOAD_ATTR (saved_profiles)
  LOAD_FAST (pid)
  BINARY_SUBSCR
  STORE_FAST (profile)

Interpretation: profile = self.saved_profiles[pid]
""")

    print("\nSTEP 2: Pattern Recognition")
    print("""
Bytecode shows:
  FOR_ITER (loop instruction)
  COMPARE_OP (<)
  LOAD_FAST (drop_count)
  LOAD_FAST (drop_limit)

Interpretation: for i in range(drop_limit):
or: while drop_count < drop_limit:
""")

    print("\nSTEP 3: String Analysis")
    print("""
Constants found:
  'https://twitter.com/login'
  'input[name="username"]'
  'input[name="password"]'
  'button[type="submit"]'

Interpretation: Uses Playwright to fill login form
Likely pattern:
  await page.goto('https://twitter.com/login')
  await page.fill('input[name="username"]', username)
  await page.fill('input[name="password"]', password)
  await page.click('button[type="submit"]')
""")

    print("\nSTEP 4: Dynamic Analysis")
    print("""
Run with instrumentation:
  [HTTP] GET https://twitter.com/login
  [BROWSER] Filling input[name="username"] = 'victim_account'
  [BROWSER] Filling input[name="password"] = 'P@ssw0rd123'
  [BROWSER] Clicking button[type="submit"]
  [WAIT] Sleeping 5 seconds
  [HTTP] POST https://twitter.com/messages/compose
  [BROWSER] Typing: 'Hit my pinned post...'

Now we KNOW the exact sequence!
""")

    print("\nSTEP 5: Confirmation")
    print("""
Cross-reference:
✓ Bytecode shows loop
✓ Strings confirm Twitter interaction
✓ Variables match Playwright patterns
✓ Dynamic trace shows actual behavior

Confidence: 95%

Reconstructed logic:
  profile = self.saved_profiles[pid]
  browser = await playwright.chromium.launch()
  page = await browser.new_page()
  await page.goto('https://twitter.com/login')
  # ... login sequence from strings
  for i in range(self.all_settings['drop_limit']):
      # ... send message sequence
      await asyncio.sleep(self.all_settings['drop_sleep'])
""")


if __name__ == '__main__':
    demonstrate_bytecode_analysis()
    show_pattern_matching()
    show_dynamic_analysis()
    show_comparative_analysis()
    show_decompiler_comparison()
    show_reverse_engineering_workflow()
    show_xbot_specific_example()

    print("\n\n" + "="*80)
    print("KEY TAKEAWAY")
    print("="*80)
    print("""
You CANNOT fully reconstruct logic from bytecode alone.
You NEED dynamic analysis (running and observing).

The combination of:
  1. Static analysis (bytecode)
  2. Dynamic analysis (execution tracing)
  3. Pattern recognition (experience)
  4. Library documentation (reference)

Gets you from 40% → 95%+ understanding.

For XBot specifically:
  - Bytecode gives structure (40%)
  - Running in VM with tracing gives behavior (80%)
  - Debugging gives exact logic (95%)
""")
