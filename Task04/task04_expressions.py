"""
Task 4 – Write Correct Expressions
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative
"""

import math

# ─── Constants ────────────────────────────────────────────────────────────────
BASE_RATE       = 30.00
BASE_FAT        = 3.5
BASE_SNF        = 8.5
FAT_STEP_VALUE  = 0.40
SNF_STEP_VALUE  = 0.30
FAT_STEP_SIZE   = 0.1
SNF_STEP_SIZE   = 0.1

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 – Core expressions for the payment calculation
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 60)
print("SECTION 1 – Core Expressions (fat=4.2, snf=8.7, litres=8.5)")
print("=" * 60)

fat, snf, litres = 4.2, 8.7, 8.5

# Number of fat steps (why round? → shown in Section 2 below)
fat_steps = round((fat - BASE_FAT) / FAT_STEP_SIZE)
snf_steps = round((snf - BASE_SNF) / SNF_STEP_SIZE)

# Rate per litre
rate = round(
    BASE_RATE
    + fat_steps * FAT_STEP_VALUE
    + snf_steps * SNF_STEP_VALUE,
    2,
)

# Amount payable
amount = round(litres * rate, 2)

print(f"  fat_steps  = round(({fat} - {BASE_FAT}) / {FAT_STEP_SIZE}) = {fat_steps}")
print(f"  snf_steps  = round(({snf} - {BASE_SNF}) / {SNF_STEP_SIZE}) = {snf_steps}")
print(f"  rate       = {BASE_RATE} + {fat_steps}×{FAT_STEP_VALUE} + {snf_steps}×{SNF_STEP_VALUE} = {rate}")
print(f"  amount     = {litres} × {rate} = {amount}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 – Surprising expression results
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 2 – Three Surprising Expression Results")
print("=" * 60)

# Surprise 1: floating-point step count
raw_steps = (4.2 - 3.5) / 0.1
print(f"\n  Surprise 1: (4.2 - 3.5) / 0.1 = {raw_steps}")
print( "  Expected 7.0, got 7.000000000000001")
print( "  Cause: 4.2 and 3.5 are not exact in IEEE 754 binary float.")
print(f"  Fix:   round({raw_steps}) = {round(raw_steps)}")

# Surprise 2: round() vs int() vs math.floor() for negative step counts
neg_val = 3.1
raw_neg = (neg_val - BASE_FAT) / FAT_STEP_SIZE   # should be -4 steps

print(f"\n  Surprise 2: Rounding a negative step count for fat={neg_val}")
print(f"    raw value         = ({neg_val} - {BASE_FAT}) / {FAT_STEP_SIZE} = {raw_neg!r}")
print(f"    round({raw_neg!r}) = {round(raw_neg)}")
print(f"    int({raw_neg!r})   = {int(raw_neg)}   ← truncates toward 0 → wrong (−3 not −4)")
print(f"    math.floor({raw_neg!r}) = {math.floor(raw_neg)} ← same as round for this value")

neg_val2 = 3.14                      # between steps
raw_neg2 = (neg_val2 - BASE_FAT) / FAT_STEP_SIZE
print(f"\n    For fat={neg_val2}: raw={raw_neg2!r}")
print(f"    round()      = {round(raw_neg2)}  (rounds to nearest, i.e. −4 steps)")
print(f"    int()        = {int(raw_neg2)}  (truncates: −3 steps → over-payment)")
print(f"    math.floor() = {math.floor(raw_neg2)}  (always down: −4 steps, same as round for .4)")

# Surprise 3: operator precedence
print("\n  Surprise 3: Operator precedence")
a, b, c = 2, 3, 4
expr1 = a + b * c          # 14, not 20
expr2 = (a + b) * c        # 20
expr3 = -b ** 2            # −9 (** binds tighter than unary minus!)
print(f"    2 + 3 * 4       = {expr1}  (expected 14 ✓)")
print(f"    (2 + 3) * 4     = {expr2}  (explicit grouping needed for 20)")
print(f"    -3 ** 2         = {expr3}  (NOT 9 — unary minus is applied AFTER **)")
print( "    -(3 ** 2) = -9, not (-3)**2 = 9")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 – Comparison chaining and Boolean operators
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 3 – Comparison Chaining and Boolean Operators")
print("=" * 60)

for test_fat in [1.5, 3.5, 4.2, 7.5]:
    valid = 2.0 <= test_fat <= 7.0
    print(f"  2.0 <= {test_fat} <= 7.0  → {valid}")

# AND / OR / NOT
fat, snf, qty = 4.2, 8.7, 10.0
entry_ok = (2.0 <= fat <= 7.0) and (7.0 <= snf <= 9.5) and (qty > 0)
print(f"\n  Entry valid (fat={fat}, snf={snf}, qty={qty})? {entry_ok}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 – Alternative: int() vs math.floor() for step count
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 4 – Alternative Step-Count Methods (complexity)")
print("=" * 60)

for f in [4.2, 3.1]:
    raw  = (f - BASE_FAT) / FAT_STEP_SIZE
    r_round = round(raw)
    r_int   = int(raw)
    r_floor = math.floor(raw)
    rate_round = round(BASE_RATE + r_round * FAT_STEP_VALUE, 2)
    rate_int   = round(BASE_RATE + r_int   * FAT_STEP_VALUE, 2)
    rate_floor = round(BASE_RATE + r_floor * FAT_STEP_VALUE, 2)
    print(f"\n  fat={f}: raw={raw!r}")
    print(f"    round()      → steps={r_round:+d}  rate=Rs {rate_round}")
    print(f"    int()        → steps={r_int:+d}  rate=Rs {rate_int}")
    print(f"    math.floor() → steps={r_floor:+d}  rate=Rs {rate_floor}")

print(
    "\n  Conclusion: round() gives the correct nearest-step count.\n"
    "  int() truncates toward 0, which under-charges for above-standard\n"
    "  fat and over-charges for below-standard fat.\n"
    "  All three methods are O(1) time and O(1) space."
)
