#!/usr/bin/env python3
"""
Extract all useful information from Python 3.13 bytecode
Works even when running on Python 3.11
"""

import marshal
import types
import struct
from pathlib import Path


def load_pyc(path):
    """Load Python 3.13 .pyc file"""
    with open(path, 'rb') as f:
        # Skip header (16 bytes for Python 3.6+)
        magic = f.read(4)
        flags = f.read(4)
        timestamp = f.read(8)

        # Load code object
        code_obj = marshal.load(f)
        return code_obj


def extract_strings(code_obj, indent=0):
    """Recursively extract all strings from code object"""
    strings = set()

    # Get constants
    if hasattr(code_obj, 'co_consts'):
        for const in code_obj.co_consts:
            if isinstance(const, str):
                strings.add(const)
            elif isinstance(const, types.CodeType):
                # Recurse into nested functions
                strings.update(extract_strings(const, indent + 1))

    return strings


def extract_names(code_obj):
    """Extract all names (variables, functions, imports)"""
    names = set()

    if hasattr(code_obj, 'co_names'):
        names.update(code_obj.co_names)

    if hasattr(code_obj, 'co_varnames'):
        names.update(code_obj.co_varnames)

    # Recurse into nested code objects
    if hasattr(code_obj, 'co_consts'):
        for const in code_obj.co_consts:
            if isinstance(const, types.CodeType):
                names.update(extract_names(const))

    return names


def extract_functions(code_obj, prefix=""):
    """Extract all function definitions"""
    functions = []

    # Current function
    if hasattr(code_obj, 'co_name'):
        name = code_obj.co_name
        argcount = getattr(code_obj, 'co_argcount', 0)
        varnames = getattr(code_obj, 'co_varnames', ())

        args = varnames[:argcount]

        func_info = {
            'name': prefix + name if prefix else name,
            'args': args,
            'varnames': varnames,
            'filename': getattr(code_obj, 'co_filename', ''),
            'lineno': getattr(code_obj, 'co_firstlineno', 0),
        }
        functions.append(func_info)

    # Recurse into nested functions
    if hasattr(code_obj, 'co_consts'):
        for const in code_obj.co_consts:
            if isinstance(const, types.CodeType):
                nested_prefix = f"{prefix}{code_obj.co_name}." if prefix or code_obj.co_name != '<module>' else ""
                functions.extend(extract_functions(const, nested_prefix))

    return functions


def main():
    pyc_path = Path('XBot.pyc')

    print("="*80)
    print("Python 3.13 Bytecode Analysis - XBot.pyc")
    print("="*80)
    print()

    # Load bytecode
    print("[*] Loading bytecode...")
    code_obj = load_pyc(pyc_path)
    print("[+] Loaded successfully")
    print()

    # Extract strings
    print("="*80)
    print("STRING CONSTANTS")
    print("="*80)
    strings = extract_strings(code_obj)
    for s in sorted(strings):
        if s and len(s) < 200:  # Skip very long strings
            print(f"  {repr(s)}")
    print()

    # Extract names
    print("="*80)
    print("NAMES (Variables, Functions, Imports)")
    print("="*80)
    names = extract_names(code_obj)
    for name in sorted(names):
        print(f"  {name}")
    print()

    # Extract functions
    print("="*80)
    print("FUNCTION DEFINITIONS")
    print("="*80)
    functions = extract_functions(code_obj)
    for func in functions:
        args_str = ', '.join(func['args'])
        print(f"  def {func['name']}({args_str}):")
        print(f"      # Local vars: {', '.join(func['varnames'])}")
        print(f"      # Line: {func['lineno']}")
        print()

    # Save detailed output
    output_path = Path('decompiled/XBot_complete_analysis.txt')
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("XBot Complete Bytecode Analysis\n")
        f.write("="*80 + "\n\n")

        f.write("STRINGS:\n")
        f.write("="*80 + "\n")
        for s in sorted(strings):
            if s:
                f.write(f"{repr(s)}\n")
        f.write("\n\n")

        f.write("NAMES:\n")
        f.write("="*80 + "\n")
        for name in sorted(names):
            f.write(f"{name}\n")
        f.write("\n\n")

        f.write("FUNCTIONS:\n")
        f.write("="*80 + "\n")
        for func in functions:
            args_str = ', '.join(func['args'])
            f.write(f"def {func['name']}({args_str}):\n")
            f.write(f"    # Local vars: {', '.join(func['varnames'])}\n")
            f.write(f"    # Line: {func['lineno']}\n")
            f.write(f"    pass\n\n")

    print(f"[+] Detailed analysis saved to: {output_path}")


if __name__ == '__main__':
    main()
