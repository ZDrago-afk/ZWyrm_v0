# cli/cli.py
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import ZWyrmEngine
from utils.banner import show_banner

def start():
    show_banner()
    ZWyrmEngine().run()