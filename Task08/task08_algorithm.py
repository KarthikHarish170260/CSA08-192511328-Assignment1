"""
Task 8 – Algorithm Planning and Pseudocode
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative

This file:
  • Contains the pseudocode as comments (SIMATS Engineering format)
  • Implements the pseudocode as Python
  • Runs a hand-trace for 3 entries
  • Compares O(n)-time / O(n)-space (list) vs O(n)-time / O(1)-space (running total)
"""

# ─────────────────────────────────────────────────────────────────────────────
# SIMATS Engineering – Standard Algorithmic Pseudocode
# ─────────────────────────────────────────────────────────────────────────────
#
# ALGORITHM  ComputeTenDayPayment
# INPUT      entries: list of (litres, fat, snf) tuples for one farmer
# OUTPUT     total: ten-day payment in Rs (2 decimal places)
#
# CONSTANTS
#   BASE_RATE      ← 30.00
#   BASE_FAT       ← 3.5
#   BASE_SNF       ← 8.5
#   FAT_STEP_VALUE ← 0.40
#   SNF_STEP_VALUE ← 0.30
#   STEP_SIZE      ← 0.1
#   FAT_MIN ← 2.0,  FAT_MAX ← 7.0
#   SNF_MIN ← 7.0,  SNF_MAX ← 9.5
#
# BEGIN
#   total ← 0.0
#   FOR EACH (litres, fat, snf) IN entries DO
#     // Step 1 – Validate
#     IF litres ≤ 0 THEN  PRINT "Invalid quantity";  CONTINUE
#     IF fat < FAT_MIN OR fat > FAT_MAX THEN  PRINT "Fat% out of range";  CONTINUE
#     IF snf < SNF_MIN OR snf > SNF_MAX THEN  PRINT "SNF% out of range";  CONTINUE
#
#     // Step 2 – Compute rate
#     fat_steps ← ROUND((fat − BASE_FAT) / STEP_SIZE)
#     snf_steps ← ROUND((snf − BASE_SNF) / STEP_SIZE)
#     rate ← ROUND(BASE_RATE + fat_steps × FAT_STEP_VALUE
#                            + snf_steps × SNF_STEP_VALUE, 2)
#
#     // Step 3 – Compute payment for this delivery
#     amount ← ROUND(litres × rate, 2)
#
#     // Step 4 – Accumulate
#     total ← total + amount
#   END FOR
#   RETURN ROUND(total, 2)
# END
#
# ─────────────────────────────────────────────────────────────────────────────
# FLOWCHART description (text representation – draw in draw.io or on paper)
# ─────────────────────────────────────────────────────────────────────────────
#
#  [START]
#    │
#    ▼
#  [READ litres, fat, snf]
#    │
#    ▼
#  ◇ litres > 0 ?
#    No  → [PRINT "Invalid quantity"] → [READ next entry]
#    Yes ↓
#  ◇ FAT_MIN ≤ fat ≤ FAT_MAX ?
#    No  → [PRINT "Fat% out of range"] → [READ next entry]
#    Yes ↓
#  ◇ SNF_MIN ≤ snf ≤ SNF_MAX ?
#    No  → [PRINT "SNF% out of range"] → [READ next entry]
#    Yes ↓
#  [Compute fat_steps, snf_steps, rate, amount]
#    │
#  [total ← total + amount]
#    │
#  ◇ More entries?
#    Yes → [READ next entry]
#    No  ↓
#  [PRINT total]
#    │
#  [STOP]
#
# ─────────────────────────────────────────────────────────────────────────────

# ─── Constants ────────────────────────────────────────────────────────────────
BASE_RATE      = 30.00
BASE_FAT       = 3.5
BASE_SNF       = 8.5
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STEP_SIZE      = 0.1
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 7.0, 9.5


# ─────────────────────────────────────────────────────────────────────────────
# Approach A: store all entries, then sum (O(n) space)
# ─────────────────────────────────────────────────────────────────────────────

def compute_total_store(entries: list) -> float:
    """
    Compute the ten-day total by STORING all valid amounts first, then summing.

    Time:  O(n) – one pass to compute amounts, one pass to sum.
    Space: O(n) – the amounts list grows with n.
    Advantage: amounts list can be inspected, printed, or re-used.
    """
    amounts = []
    for litres, fat, snf in entries:
        if litres <= 0: continue
        if not (FAT_MIN <= fat <= FAT_MAX): continue
        if not (SNF_MIN <= snf <= SNF_MAX): continue
        fat_steps = round((fat - BASE_FAT) / STEP_SIZE)
        snf_steps = round((snf - BASE_SNF) / STEP_SIZE)
        rate   = round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
        amount = round(litres * rate, 2)
        amounts.append(amount)
    return round(sum(amounts), 2)


# ─────────────────────────────────────────────────────────────────────────────
# Approach B: running total (O(1) space)
# ─────────────────────────────────────────────────────────────────────────────

def compute_total_running(entries: list) -> float:
    """
    Compute the ten-day total with a RUNNING TOTAL (no stored amounts list).

    Time:  O(n) – single pass.
    Space: O(1) – only one accumulator variable regardless of n.
    Best when n is very large (150,000 entries) and individual amounts
    are not needed after the run.
    """
    total = 0.0
    for litres, fat, snf in entries:
        if litres <= 0: continue
        if not (FAT_MIN <= fat <= FAT_MAX): continue
        if not (SNF_MIN <= snf <= SNF_MAX): continue
        fat_steps = round((fat - BASE_FAT) / STEP_SIZE)
        snf_steps = round((snf - BASE_SNF) / STEP_SIZE)
        rate   = round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
        total += round(litres * rate, 2)
    return round(total, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Hand trace for 3 entries
# ─────────────────────────────────────────────────────────────────────────────

def hand_trace():
    """Print a step-by-step trace for three entries."""
    entries = [
        (10.0, 3.5, 8.5),   # standard milk
        ( 8.5, 4.2, 8.7),   # above standard
        (12.0, 3.1, 8.3),   # below standard
    ]

    print("=" * 70)
    print("HAND TRACE – ComputeTenDayPayment")
    print("=" * 70)
    print(f"{'#':>2} {'litres':>7} {'fat':>5} {'snf':>5} {'fat_s':>6} {'snf_s':>6} "
          f"{'rate':>7} {'amount':>9} {'running_total':>14}")
    print("-" * 70)

    running = 0.0
    for i, (litres, fat, snf) in enumerate(entries, 1):
        fat_steps = round((fat - BASE_FAT) / STEP_SIZE)
        snf_steps = round((snf - BASE_SNF) / STEP_SIZE)
        rate   = round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
        amount = round(litres * rate, 2)
        running += amount
        print(f"{i:>2} {litres:>7.1f} {fat:>5.2f} {snf:>5.2f} {fat_steps:>6} {snf_steps:>6} "
              f"{rate:>7.2f} {amount:>9.2f} {running:>14.2f}")

    print("-" * 70)
    print(f"{'Ten-day total':>62}  {running:>9.2f}")
    print("=" * 70)


if __name__ == "__main__":
    hand_trace()

    # Demonstrate both approaches give the same result
    entries = [(10.0, 3.5, 8.5), (8.5, 4.2, 8.7), (12.0, 3.1, 8.3)]
    t1 = compute_total_store(entries)
    t2 = compute_total_running(entries)
    print(f"\nApproach A (store then sum):  Rs {t1}")
    print(f"Approach B (running total):   Rs {t2}")
    print(f"Results match: {t1 == t2}")
    print(
        "\nComplexity comparison:\n"
        "  Approach A: O(n) time, O(n) space – store amounts for later use\n"
        "  Approach B: O(n) time, O(1) space – best for streaming large datasets\n"
        "  Storing entries is still needed when:\n"
        "    • Entries must be audited or reprinted\n"
        "    • Statistics (min, max, average) are required after the run\n"
        "    • Entries may need correction and re-processing"
    )
