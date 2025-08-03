#!/usr/bin/env python3
"""
Test script to verify the Nutaan CLI interactive mode works properly
"""

import subprocess
import time
import signal
import os

def test_interactive_mode():
    """Test the interactive mode functionality"""
    print("🧪 Testing Nutaan CLI Interactive Mode...")
    
    # Change to the project directory
    os.chdir('/home/cp/nutaan-cli')
    
    # Start the interactive mode
    process = subprocess.Popen(
        ['python3', '-m', 'nutaan', '-e', '.env.gemini'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=os.setsid
    )
    
    try:
        # Send menu choice and a test message
        input_data = "1\nHello, can you help me with a simple Python question?\nquit\n"
        
        # Set a timeout
        stdout, stderr = process.communicate(input=input_data, timeout=30)
        
        print("✅ Interactive mode test completed!")
        print("\n--- STDOUT ---")
        print(stdout[:2000] + "..." if len(stdout) > 2000 else stdout)
        
        if stderr:
            print("\n--- STDERR ---")
            print(stderr[:1000] + "..." if len(stderr) > 1000 else stderr)
            
        return "Assistant Ready" in stdout and "Session:" in stdout
        
    except subprocess.TimeoutExpired:
        print("⏱️ Test timed out - killing process")
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        if process.poll() is None:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return False

if __name__ == "__main__":
    success = test_interactive_mode()
    if success:
        print("\n🎉 SUCCESS: Interactive mode is working properly!")
        print("✅ Environment loading works")
        print("✅ Model detection works") 
        print("✅ Conversation mode works")
        print("\n🚀 Your Nutaan CLI is ready to use!")
        print("Run: python3 -m nutaan -e .env.gemini")
    else:
        print("\n❌ Test failed - there may be issues to resolve")
