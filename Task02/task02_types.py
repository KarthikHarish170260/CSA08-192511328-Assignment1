"""
Task 2 – Explore Values and Types in the Interpreter
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative

This script demonstrates the interactive-mode explorations required for Task 2.
Run it directly; the output mirrors what you would see at the >>> prompt.
"""

# ─────────────────────────────────────────────
# 2.1  Types of common values
# ─────────────────────────────────────────────
print("=" * 60)
print("SECTION 1 – Types of Values")
print("=" * 60)

values = [10, 10.0, "10", True, [10, 8.5]]
for v in values:
    print(f"  type({v!r:12}) → {type(v).__name__}")

# ─────────────────────────────────────────────
# 2.2  Division operators
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 2 – Division Operators")
print("=" * 60)

print(f"  7 / 2   = {7 / 2}   (true division → float)")
print(f"  7 // 2  = {7 // 2}   (floor division → int, rounds toward −∞)")
print(f"  7 % 2   = {7 % 2}   (modulo / remainder)")
print(f" -7 // 2  = {-7 // 2}   (floor division on negative → floors to −4, not −3!)")
print(f" -7 %  2  = {-7 % 2}   (follows floor-division: -7 = (-4)*2 + 1)")

# Explanation: Python's // always floors toward negative infinity.
# In C or Java, integer division truncates toward zero, giving -3.
# That is why -7 // 2 == -4 in Python, not -3.

# ─────────────────────────────────────────────
# 2.3  Floating-point surprise
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 3 – Floating-Point Representation Issue")
print("=" * 60)

result = 0.1 + 0.2 == 0.3
print(f"  0.1 + 0.2 == 0.3  → {result}")
print(f"  0.1 + 0.2         = {0.1 + 0.2!r}")
print(f"  0.3               = {0.3!r}")
print()
print("  Explanation: IEEE 754 double-precision floats cannot represent")
print("  0.1 or 0.2 exactly in binary.  Their stored values differ from")
print("  the true decimal values by tiny fractions, so their sum is")
print("  0.30000000000000004, not 0.3.")

# ─────────────────────────────────────────────
# 2.4  Why float rupees are dangerous for money
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("SECTION 4 – Money Arithmetic Errors and Fixes")
print("=" * 60)

# Demonstrate the drift
total = 0.0
for _ in range(300):          # 300 payments of Rs 33.40
    total += 33.40

print(f"  300 × 33.40  (float sum)  = {total:.6f}   ← wrong!")
print(f"  300 × 33.40  (expected)   = {300 * 33.40:.6f}")

# Fix 1: integer paise
total_paise = 0
for _ in range(300):
    total_paise += 3340        # 33.40 × 100

print(f"\n  Fix 1 – integer paise    : {total_paise} paise = Rs {total_paise / 100:.2f}")

# Fix 2: round() after every addition
total_round = 0.0
for _ in range(300):
    total_round = round(total_round + 33.40, 2)

print(f"  Fix 2 – round() each add : Rs {total_round:.2f}")

# Fix 3: Decimal (shown in task02_decimal.py)
print(f"  Fix 3 – Decimal module   : see task02_decimal.py")

print("\nConclusion: Use integer paise or the Decimal module for exact")
print("money arithmetic; float is only acceptable for rough estimates.")
