#!/usr/bin/env python3
"""
Test for Google Gemini content block format handling.

Tests the _safe_content_str() function with Google's specific content format
that includes thought signatures and extras.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nutaan.cli import _safe_content_str


def test_google_content_format():
    """Test Google Gemini content block format."""
    
    # Real Google Gemini response format (from user's error)
    google_content = [
        {
            'type': 'text',
            'text': 'I am Gemini, a large language model built by Google.',
            'extras': {
                'signature': 'Es4DCssDAdHtim+I8qRx6FGklxq6lDej9a7jMmQtJWKK+eZaEE3TiexLJlbdmcVquf4FZNxDXgzk2mk3PU14MeyhKzP2KCevzF23CjfEIu+QxBZGu+A6tmX7VlRLcs5SU7cNma57OotDdAJiyyGIk5pXjlkH9jIrMvjGY0EmGGvR+ICXeeS30vM7OOO6Zwa2+Yqbft1NZJOLAl3WokUwvt42sVmtGXPJWqt4bXfRmp3xEtxcH8QXQjbaJ7F64DSiWxpIX/lJc+fcHPBrbxuXKLlIspmb19wt+hw6Lb2I/k/r92Fc/6TH4vacQVFLQWlKvLqQooMnTrc6a5pRwSSnPKWd0mv8mqttDCH5+/BET33j/1ZZt/WL4LO7ceu1bynATAhVKnbFvUrFPXufSj8Br4oavNsTSmZw8Cn271iFGATytFr2TdosHCrPF2LuSO4JT8sKhr40vbL2lzopyloNqwo3sabpDTY0NFyP4XEXoOjUB2OMJ6guAqzoMDPyqbw8HZjzbPp7GoO/+97r/v96QAtgkq1tSKZY8D+9O2zbK26+e+4k7EwnYRu5sRDhzx8DzJORbiSrY42PBD5MerXR4txzDuRKb3bN5GwJ2oWm05JN'
            }
        }
    ]
    
    result = _safe_content_str(google_content)
    expected = 'I am Gemini, a large language model built by Google.'
    
    print("Test 1: Google Gemini content format")
    print(f"Input: {google_content[0]['type']}, text length: {len(google_content[0]['text'])}")
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    
    if result == expected:
        print("✅ Google content format test passed!\n")
    else:
        print(f"❌ FAILED: Expected '{expected}', got '{result}'\n")
        return False
    
    # Test multiple content blocks
    multi_block = [
        {'type': 'text', 'text': 'First part.', 'extras': {'signature': 'abc123'}},
        {'type': 'text', 'text': 'Second part.', 'extras': {'signature': 'def456'}}
    ]
    
    result = _safe_content_str(multi_block)
    expected = 'First part. Second part.'
    
    print("Test 2: Multiple Google content blocks")
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    
    if result == expected:
        print("✅ Multiple blocks test passed!\n")
    else:
        print(f"❌ FAILED: Expected '{expected}', got '{result}'\n")
        return False
    
    # Test mixed content (Google + other)
    mixed = [
        {'type': 'text', 'text': 'Hello', 'extras': {}},
        'plain string',
        {'text': 'world'}  # Missing 'type' field
    ]
    
    result = _safe_content_str(mixed)
    print("Test 3: Mixed content formats")
    print(f"Result: {result}")
    
    if 'Hello' in result and 'plain string' in result and 'world' in result:
        print("✅ Mixed content test passed!\n")
    else:
        print(f"❌ FAILED: Missing expected content in '{result}'\n")
        return False
    
    # Test simple string (backward compatibility)
    simple = "Just a simple string"
    result = _safe_content_str(simple)
    
    print("Test 4: Simple string (backward compatibility)")
    print(f"Result: {result}")
    
    if result == simple:
        print("✅ Simple string test passed!\n")
    else:
        print(f"❌ FAILED: Expected '{simple}', got '{result}'\n")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Google Gemini Content Format Handling")
    print("=" * 60 + "\n")
    
    if test_google_content_format():
        print("🎉 All Google content format tests passed!")
        print("The Google Gemini integration should now display clean text.")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
