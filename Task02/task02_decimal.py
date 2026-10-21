"""
Task 2 – Complete the Code  (Decimal vs float totalling)
CSA0807 Python Programming Assignment 1

Expected output:
    float  : 33400.30000000061
    Decimal: 33400.30
    False True
"""

from decimal import Decimal
import sys

# 1,000 payments of Rs 33.40 and three small adjustments of Rs 0.10
payments = ["33.40"] * 1000 + ["0.10"] * 3


def total_float(items):
    """Sum amounts as plain Python floats (demonstrates accumulated error)."""
    total = 0.0
    for amount in items:
        total += float(amount)
    return total


def total_decimal(items):
    """
    Sum amounts exactly using the Decimal type.

    Each string is converted directly to Decimal (NOT via float) so that no
    floating-point rounding error is introduced before the addition.
    Returns the exact Decimal total.
    """
    # TODO 1 – solution ↓
    total = Decimal("0")
    for amount in items:
        total += Decimal(amount)   # create Decimal FROM THE STRING, not from float(amount)
    return total


print("float  :", total_float(payments))
print("Decimal:", total_decimal(payments))
print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

# ─────────────────────────────────────────────────────────────────────────────
# What happens when you write Decimal(float(amount)) instead?
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- Effect of Decimal(float(amount)) ---")
bad_total = Decimal(0)
for amount in payments:
    bad_total += Decimal(float(amount))   # float error is baked in first!

print("Decimal(float(amount)) total:", bad_total)
print(
    "\nExplanation: float(\"33.40\") gives 33.399999999999999289 (the nearest\n"
    "IEEE 754 double), and Decimal() faithfully preserves that inexact value.\n"
    "So the error from floating-point representation is introduced BEFORE\n"
    "Decimal can help; the result looks like 33400.29999999999927240..."
)

# ─────────────────────────────────────────────────────────────────────────────
# Alternative Concept – integer paise and sys.getsizeof() comparison
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- Memory comparison (sys.getsizeof) ---")
a_float   = 33.40
a_int     = 3340           # paise
a_decimal = Decimal("33.40")

print(f"  float   value: {a_float}   size: {sys.getsizeof(a_float)} bytes")
print(f"  int     value: {a_int}      size: {sys.getsizeof(a_int)} bytes")
print(f"  Decimal value: {a_decimal}  size: {sys.getsizeof(a_decimal)} bytes")

print(
    "\nConclusion:\n"
    "  • Integer paise  – exact, fastest addition, smallest memory.\n"
    "  • Decimal string – exact, slightly slower, larger memory, most readable.\n"
    "  • float + round()– approximate; round() after EVERY addition avoids\n"
    "    drift for small counts but is fragile at 150,000-entry scale."
)
