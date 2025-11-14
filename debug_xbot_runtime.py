#!/usr/bin/env python3
"""
Runtime instrumentation to capture XBot behavior
This shows how you'd debug bytecode by watching it execute
"""

import sys
import dis
import marshal
from types import CodeType


class BytecodeDebugger:
    """
    Instruments Python bytecode to log all operations
    """

    def __init__(self):
        self.execution_log = []
        self.function_calls = []
        self.variable_values = {}

    def trace_calls(self, frame, event, arg):
        """
        Trace function that gets called for every line of code
        """
        if event == 'call':
            # A function is being called
            code = frame.f_code
            func_name = code.co_filename + ":" + code.co_name
            args = frame.f_locals.copy()

            self.function_calls.append({
                'function': code.co_name,
                'file': code.co_filename,
                'line': frame.f_lineno,
                'arguments': args
            })

            print(f"[CALL] {code.co_name}() at line {frame.f_lineno}")
            print(f"       Arguments: {list(args.keys())}")

        elif event == 'line':
            # A line of code is being executed
            code = frame.f_code
            print(f"[LINE] {code.co_name}:{frame.f_lineno}")

        elif event == 'return':
            # Function is returning
            print(f"[RETURN] {frame.f_code.co_name} -> {arg}")

        return self.trace_calls

    def run_with_trace(self, code_obj):
        """
        Run bytecode with full tracing enabled
        """
        print("="*80)
        print("STARTING INSTRUMENTED EXECUTION")
        print("="*80)
        print()

        # Set the trace function
        sys.settrace(self.trace_calls)

        try:
            # Execute the bytecode
            exec(code_obj)
        except Exception as e:
            print(f"\n[ERROR] {type(e).__name__}: {e}")
        finally:
            sys.settrace(None)

        print()
        print("="*80)
        print("EXECUTION COMPLETE")
        print("="*80)
        print(f"Total function calls: {len(self.function_calls)}")


class VariableWatcher:
    """
    Watches specific variables and logs their values
    """

    def __init__(self, watch_names):
        self.watch_names = watch_names
        self.history = {name: [] for name in watch_names}

    def trace_variables(self, frame, event, arg):
        """
        Log variable values whenever they change
        """
        if event in ('line', 'call', 'return'):
            for name in self.watch_names:
                if name in frame.f_locals:
                    value = frame.f_locals[name]
                    self.history[name].append({
                        'line': frame.f_lineno,
                        'value': value,
                        'type': type(value).__name__
                    })
                    print(f"[VAR] {name} = {repr(value)[:80]}")

        return self.trace_variables


def demonstrate_debugging():
    """
    Show how debugging would work on XBot
    """
    print("="*80)
    print("Python Debugger Demonstration")
    print("="*80)
    print()

    # Example: What we'd do with XBot.pyc
    print("STEP 1: Load XBot.pyc bytecode")
    print("----------------------------------------")
    print("import marshal")
    print("with open('XBot.pyc', 'rb') as f:")
    print("    f.read(16)  # Skip header")
    print("    code = marshal.load(f)")
    print()

    print("STEP 2: Set up instrumentation")
    print("----------------------------------------")
    print("import sys")
    print("debugger = BytecodeDebugger()")
    print("sys.settrace(debugger.trace_calls)")
    print()

    print("STEP 3: Execute and watch")
    print("----------------------------------------")
    print("exec(code)  # This runs XBot")
    print()
    print("Now we'd see:")
    print("  [CALL] __init__() at line 50")
    print("  [LINE] __init__:51")
    print("  [VAR] self.runner = <AsyncRunner>")
    print("  [VAR] self.accounts = []")
    print("  [CALL] _load_profiles_local() at line 100")
    print("  [LINE] _load_profiles_local:101")
    print("  [VAR] f = <file object>")
    print("  [VAR] content = '{\"profiles\": [...]}' ")
    print("  [RETURN] _load_profiles_local -> None")
    print()

    print("STEP 4: Capture interesting data")
    print("----------------------------------------")
    print("We'd log:")
    print("  - Every API endpoint called")
    print("  - All passwords/tokens in memory")
    print("  - Twitter login flow")
    print("  - Message content being sent")
    print("  - File read/write operations")
    print()


def show_pdb_example():
    """
    Show how Python's built-in debugger works
    """
    print("="*80)
    print("Example: Python's pdb Debugger")
    print("="*80)
    print()

    print("If we had XBot source code, we'd do:")
    print()
    print("```python")
    print("import pdb")
    print()
    print("class XBotApp:")
    print("    def _run_automation(self, pid):")
    print("        pdb.set_trace()  # <-- Pause here!")
    print("        browser = await playwright.chromium.launch()")
    print("        page = await browser.new_page()")
    print("```")
    print()
    print("When execution hits pdb.set_trace(), you get an interactive prompt:")
    print()
    print("(Pdb) print(pid)")
    print("'profile_123'")
    print()
    print("(Pdb) print(browser)")
    print("<Browser chromium>")
    print()
    print("(Pdb) next  # Execute next line")
    print("(Pdb) step  # Step into function")
    print("(Pdb) continue  # Keep running")
    print()


def show_practical_approach():
    """
    Show the actual practical approach for XBot
    """
    print("="*80)
    print("PRACTICAL APPROACH FOR XBOT")
    print("="*80)
    print()

    print("Since traditional debugging is hard with bytecode,")
    print("here's what security researchers actually do:")
    print()

    print("METHOD 1: Dynamic Analysis (Best for XBot)")
    print("----------------------------------------")
    print("1. Run XBot in a sandbox VM")
    print("2. Use system monitoring tools:")
    print("   - Process Monitor (Windows) - See file/registry access")
    print("   - Wireshark - Capture network traffic")
    print("   - API Monitor - Log all API calls")
    print("   - Memory dumps - Extract data from RAM")
    print()
    print("What you'd capture:")
    print("  ✓ Twitter API endpoints called")
    print("  ✓ Credentials sent over network")
    print("  ✓ Files read/written")
    print("  ✓ Browser automation patterns")
    print()

    print("METHOD 2: Monkey Patching")
    print("----------------------------------------")
    print("Intercept Python functions before XBot uses them:")
    print()
    print("```python")
    print("import httpx")
    print()
    print("# Save original function")
    print("original_get = httpx.AsyncClient.get")
    print()
    print("# Replace with logging version")
    print("async def logged_get(self, url, **kwargs):")
    print("    print(f'[HTTP GET] {url}')")
    print("    print(f'[HEADERS] {kwargs.get(\"headers\")}')")
    print("    return await original_get(self, url, **kwargs)")
    print()
    print("httpx.AsyncClient.get = logged_get")
    print()
    print("# Now run XBot - all HTTP calls are logged!")
    print("import XBot")
    print("```")
    print()

    print("METHOD 3: Frida (Advanced)")
    print("----------------------------------------")
    print("Inject JavaScript into Python runtime:")
    print("  - Hook any function at runtime")
    print("  - Modify behavior on the fly")
    print("  - Extract data from memory")
    print()
    print("Example:")
    print("  Interceptor.attach(ptr(playwright_address), {")
    print("    onEnter: function(args) {")
    print("      console.log('Playwright called with: ' + args[0]);")
    print("    }")
    print("  });")
    print()


if __name__ == '__main__':
    demonstrate_debugging()
    print("\n")
    show_pdb_example()
    print("\n")
    show_practical_approach()
