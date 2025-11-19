#!/usr/bin/env python3
"""Test the content fix for list vs string handling"""

import sys
sys.path.insert(0, '/home/tecosys/nutaan-cli')

# Test the helper function
from nutaan.cli import _safe_content_str

# Test cases
test_cases = [
    ("Simple string", "hello world", "hello world"),
    ("List of strings", ["hello", "world"], "hello world"),
    ("List with mixed types", ["test", 123, "data"], "test 123 data"),
    ("Empty string", "", ""),
    ("Empty list", [], ""),
    ("None", None, ""),
]

print("Testing _safe_content_str helper function:\n")
all_passed = True

for name, input_val, expected in test_cases:
    result = _safe_content_str(input_val)
    passed = result == expected
    status = "✅" if passed else "❌"
    
    print(f"{status} {name}")
    print(f"   Input: {repr(input_val)}")
    print(f"   Expected: {repr(expected)}")
    print(f"   Got: {repr(result)}")
    
    if not passed:
        all_passed = False
    print()

if all_passed:
    print("🎉 All tests passed!")
    print("\nThe migration fix is working correctly.")
    print("The application should now handle both string and list content.")
else:
    print("⚠️  Some tests failed")
    sys.exit(1)
