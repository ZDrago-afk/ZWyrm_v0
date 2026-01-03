#!/usr/bin/env python3
"""
ZWyrm - Main Entry Point
Red-Team–Informed Behavioral Antivirus for Linux
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try different import methods
try:
    # First try direct import
    from cli import start
except ImportError:
    try:
        # Try alternative
        from cli.cli import start
    except ImportError as e:
        print(f"[!] Import error: {e}")
        print("[!] Make sure cli/ folder contains __init__.py and cli.py")
        sys.exit(1)

def main():
    """Main entry point for ZWyrm."""
    try:
        start()
    except KeyboardInterrupt:
        print("\n[!] ZWyrm stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()