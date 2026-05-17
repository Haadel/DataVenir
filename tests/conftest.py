import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Ensure project root is on sys.path so tests can import `src.*`
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

