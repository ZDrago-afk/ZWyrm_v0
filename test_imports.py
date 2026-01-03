#!/usr/bin/env python3
"""Test script to verify all imports work correctly"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    from cli import start
    print("✓ Imported from cli")
except ImportError as e:
    print(f"✗ Failed to import from cli: {e}")

try:
    from core.engine import ZWyrmEngine
    print("✓ Imported ZWyrmEngine from core.engine")
except ImportError as e:
    print(f"✗ Failed to import ZWyrmEngine: {e}")

try:
    from utils.banner import show_banner
    print("✓ Imported show_banner from utils.banner")
except ImportError as e:
    print(f"✗ Failed to import show_banner: {e}")

try:
    import psutil
    print("✓ Imported psutil")
except ImportError as e:
    print(f"✗ Failed to import psutil: {e}")

try:
    import yaml
    print("✓ Imported yaml")
except ImportError as e:
    print(f"✗ Failed to import yaml: {e}")

try:
    from rich.console import Console
    print("✓ Imported rich")
except ImportError as e:
    print(f"✗ Failed to import rich: {e}")

print("\nAll imports tested.")