"""
Task 3 – Variables, Constants and Dynamic Typing
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative
"""

# ─────────────────────────────────────────────────────────────────────────────
# Named constants  (UPPER_CASE by PEP 8 convention)
# Python has no built-in 'const' keyword; convention + discipline enforces it.
# ─────────────────────────────────────────────────────────────────────────────

BASE_RATE        = 30.00   # Rs per litre for 3.5 % fat / 8.5 % SNF milk
BASE_FAT         = 3.5     # % – reference fat level
BASE_SNF         = 8.5     # % – reference SNF level
FAT_STEP_VALUE   = 0.40    # Rs per 0.1 % fat deviation
SNF_STEP_VALUE   = 0.30    # Rs per 0.1 % SNF deviation
FAT_STEP_SIZE    = 0.1     # % – size of one fat step
SNF_STEP_SIZE    = 0.1     # % – size of one SNF step
FAT_MIN          = 2.0     # % – lowest accepted fat reading
FAT_MAX          = 7.0     # % – highest accepted fat reading
SNF_MIN          = 7.0     # % – lowest accepted SNF reading
SNF_MAX          = 9.5     # % – highest accepted SNF reading
QTY_MIN          = 0.0     # litres – minimum accepted quantity (exclusive)
PAYMENT_DAYS     = 10      # number of days in one payment cycle

# ─────────────────────────────────────────────────────────────────────────────
# Demonstration: naming rules and conventions
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 60)
print("SECTION 1 – Named Constants (rate card)")
print("=" * 60)
print(f"  BASE_RATE      = {BASE_RATE} Rs/litre")
print(f"  FAT_STEP_VALUE = {FAT_STEP_VALUE} Rs per 0.1 % deviation")
print(f"  SNF_STEP_VALUE = {SNF_STEP_VALUE} Rs per 0.1 % deviation")
print(f"  FAT range      = [{FAT_MIN}, {FAT_MAX}] %")
print(f"  SNF range      = [{SNF_MIN}, {SNF_MAX}] %")

# ─────────────────────────────────────────────────────────────────────────────
# Demonstration: dynamic typing
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 2 – Dynamic Typing")
print("=" * 60)

x = 42
print(f"  x = {x!r}  → type: {type(x).__name__}")

x = "forty-two"
print(f"  x = {x!r}  → type: {type(x).__name__}")

x = [42, 3.5, True]
print(f"  x = {x!r}  → type: {type(x).__name__}")

print(
    "\n  Explanation: Python does NOT have typed variable declarations.\n"
    "  The variable 'x' can hold any object; its type is the type of the\n"
    "  object it currently references.  This is called dynamic typing.\n"
    "  For a payment calculator it means a bug such as\n"
    "      fat = input('Fat%: ')   # returns str, not float!\n"
    "  will not raise an error until fat is used in arithmetic."
)

# ─────────────────────────────────────────────────────────────────────────────
# Demonstration: multiple assignment and swap
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 3 – Multiple Assignment and Swap")
print("=" * 60)

a, b = 3.5, 8.5
print(f"  Before swap: a={a}, b={b}")
a, b = b, a
print(f"  After  swap: a={a}, b={b}")
print("  (Python evaluates the right side as a tuple FIRST, then unpacks)")

farmer_id, litres, fat, snf = "F001", 10.0, 4.2, 8.7
print(f"\n  Unpacked entry: farmer={farmer_id}, litres={litres}, fat={fat}, snf={snf}")

# ─────────────────────────────────────────────────────────────────────────────
# Alternative: rate values embedded as magic numbers vs RATE_CARD dict
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 4 – Alternative: RATE_CARD dictionary")
print("=" * 60)

RATE_CARD = {
    "base"     : 30.00,
    "fat_step" : 0.40,
    "snf_step" : 0.30,
    "fat_base" : 3.5,
    "snf_base" : 8.5,
}

fat, snf = 4.2, 8.7
fat_steps = round((fat - RATE_CARD["fat_base"]) / 0.1)
snf_steps = round((snf - RATE_CARD["snf_base"]) / 0.1)
rate = round(
    RATE_CARD["base"]
    + fat_steps * RATE_CARD["fat_step"]
    + snf_steps * RATE_CARD["snf_step"],
    2,
)
print(f"  Rate from RATE_CARD for fat={fat}, snf={snf}: Rs {rate}")
print(
    "\n  Trade-off:\n"
    "  • RATE_CARD groups all rates in one dict – a single place to change.\n"
    "  • Named constants are equally centralised but more readable.\n"
    "  • Magic numbers scattered in code require k changes for a revision;\n"
    "    missing even one creates a silent, hard-to-find bug.\n"
    "  Time complexity of a revision: O(k) for magic numbers, O(1) for\n"
    "  a named constant or RATE_CARD.  Memory cost is negligible either way."
)
