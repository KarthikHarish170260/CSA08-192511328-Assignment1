"""
Task 7 – Use the milkrate module from a separate script
CSA0807 Python Programming Assignment 1

Run with:  python Task07/use_milkrate.py
(milkrate.py must be in the same folder, or on sys.path)
"""

import sys
import os

# Ensure the script can find milkrate.py when run from the repo root.
# (Python searches the directory of the running script first, so if you
#  run from inside Task07/ this line is not needed.)
sys.path.insert(0, os.path.dirname(__file__))

import milkrate                         # import style 1
from milkrate import payout             # import style 2
import milkrate as mr                   # import style 3

print("=" * 60)
print("TASK 7 – Importing milkrate three ways")
print("=" * 60)

# Style 1: milkrate.rate_per_litre()
print("\nStyle 1 – import milkrate:")
r = milkrate.rate_per_litre(4.2, 8.7)
print(f"  milkrate.rate_per_litre(4.2, 8.7) = Rs {r}")

# Style 2: from milkrate import payout
print("\nStyle 2 – from milkrate import payout:")
p = payout(8.5, 4.2, 8.7)
print(f"  payout(8.5, 4.2, 8.7) = Rs {p}")

# Style 3: import milkrate as mr
print("\nStyle 3 – import milkrate as mr:")
r2 = mr.rate_per_litre(3.1, 8.3)
p2 = mr.payout(12, 3.1, 8.3)
print(f"  mr.rate_per_litre(3.1, 8.3) = Rs {r2}")
print(f"  mr.payout(12, 3.1, 8.3)     = Rs {p2}")

# ── Why the self-test table is NOT printed ────────────────────────────────────
print("\n" + "=" * 60)
print("Why the self-test table is absent")
print("=" * 60)
print(f"  milkrate.__name__ = {milkrate.__name__!r}")
print(
    "  When Python imports a module, __name__ is set to the module's\n"
    "  file name (without .py).  The 'if __name__ == \"__main__\":' block\n"
    "  in milkrate.py therefore does NOT run.  This prevents unwanted\n"
    "  side-effects (printing, sleeping, opening files) on import."
)

# ── sys.path lookup order ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Where Python looks for milkrate (sys.path order)")
print("=" * 60)
for i, p in enumerate(sys.path[:6]):
    print(f"  [{i}] {p}")
print("  ... (PYTHONPATH and site-packages follow)")
print(
    "\n  Python searches these directories in order.  It found milkrate.py\n"
    "  in directory [0] (the script's own folder, added by sys.path.insert)."
)

# ── Complexity note on module import ─────────────────────────────────────────
print("\n" + "=" * 60)
print("Import cost (alternative: copy-paste vs import)")
print("=" * 60)
print(
    "  Python loads a module ONCE and caches it in sys.modules.\n"
    "  Subsequent 'import milkrate' statements return the cached object\n"
    "  immediately (O(1) dict lookup).  The first-time parse/compile cost\n"
    "  is O(size of milkrate.py) – negligible for a small module.\n\n"
    "  If the functions were copy-pasted into every script:\n"
    "  • A rate revision requires editing k files (k = number of scripts).\n"
    "  • One missed file silently produces wrong payments.\n"
    "  • The module approach keeps the change to ONE file, O(1) edits."
)
