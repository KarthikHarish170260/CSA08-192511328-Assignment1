"""
Task 9 – Implement and Test the Calculator
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative

Run with:  python Task09/task09_calculator.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Task07'))
from milkrate import rate_per_litre, payout

# ─── Additional constants ─────────────────────────────────────────────────────
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 7.0, 9.5


def validate_entry(litres, fat, snf):
    """Return list of error strings; empty → valid."""
    errors = []
    if not isinstance(litres, (int, float)) or litres <= 0:
        errors.append(f"litres={litres} must be > 0")
    if not isinstance(fat, (int, float)) or not (FAT_MIN <= fat <= FAT_MAX):
        errors.append(f"fat={fat} must be in [{FAT_MIN}, {FAT_MAX}]")
    if not isinstance(snf, (int, float)) or not (SNF_MIN <= snf <= SNF_MAX):
        errors.append(f"snf={snf} must be in [{SNF_MIN}, {SNF_MAX}]")
    return errors


def ten_day_total(entries):
    """Sum payout() for each valid entry; skip invalid with a warning."""
    total = 0.0
    for litres, fat, snf in entries:
        errs = validate_entry(litres, fat, snf)
        if errs:
            print(f"  [SKIP] ({litres}, {fat}, {snf}): {'; '.join(errs)}")
            continue
        total += payout(litres, fat, snf)
    return round(total, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Test suite using assert statements
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    """Run all test cases and report results."""
    PASS, FAIL = 0, 0

    def check(label, actual, expected, tol=0.001):
        nonlocal PASS, FAIL
        ok = abs(actual - expected) < tol
        status = "PASS ✓" if ok else f"FAIL ✗  (got {actual}, expected {expected})"
        print(f"  {label:55} {status}")
        if ok: PASS += 1
        else:  FAIL += 1

    def check_errors(label, litres, fat, snf, expect_errors):
        nonlocal PASS, FAIL
        errs = validate_entry(litres, fat, snf)
        ok = bool(errs) == expect_errors
        status = "PASS ✓" if ok else f"FAIL ✗  (errors={errs})"
        print(f"  {label:55} {status}")
        if ok: PASS += 1
        else:  FAIL += 1

    print("=" * 70)
    print("TASK 9 – Test Table")
    print("=" * 70)

    # ── Group 1: Normal entries ───────────────────────────────────────────────
    print("\n[1] Normal entries")
    check("Standard milk (3.5%, 8.5%)  rate",        rate_per_litre(3.5, 8.5), 30.00)
    check("Above standard fat (4.2%)   rate",         rate_per_litre(4.2, 8.5), 32.80)
    check("Above standard fat+snf      rate",         rate_per_litre(4.2, 8.7), 33.40)
    check("Below standard fat (3.1%)   rate",         rate_per_litre(3.1, 8.5), 28.40)
    check("Below standard snf (8.3%)   rate",         rate_per_litre(3.5, 8.3), 29.40)
    check("Both below standard         rate",         rate_per_litre(3.1, 8.3), 27.80)

    check("payout(10, 3.5, 8.5)  =  300.00",         payout(10, 3.5, 8.5),   300.00)
    check("payout(8.5, 4.2, 8.7) =  283.90",         payout(8.5, 4.2, 8.7),  283.90)
    check("payout(12, 3.1, 8.3)  =  333.60",         payout(12, 3.1, 8.3),   333.60)

    # ── Group 2: Boundary entries ─────────────────────────────────────────────
    print("\n[2] Boundary entries")
    check("Exact standard (3.5%, 8.5%) – lowest bonus", rate_per_litre(3.5, 8.5), 30.00)
    check("Lowest fat boundary (2.0%)  rate",            rate_per_litre(2.0, 8.5), 24.00)
    check("Highest fat boundary (7.0%) rate",            rate_per_litre(7.0, 8.5), 44.00)
    check("Lowest snf boundary (7.0%)  rate",            rate_per_litre(3.5, 7.0), 25.50)
    check("Highest snf boundary (9.5%) rate",            rate_per_litre(3.5, 9.5), 34.50)

    # ── Group 3: Invalid entries ──────────────────────────────────────────────
    print("\n[3] Invalid entries (validate_entry must detect errors)")
    check_errors("Negative quantity (-1, 3.5, 8.5)",         -1,   3.5, 8.5, True)
    check_errors("Zero quantity (0, 3.5, 8.5)",               0,   3.5, 8.5, True)
    check_errors("Fat too low (10, 1.5, 8.5)",               10,   1.5, 8.5, True)
    check_errors("Fat too high (10, 8.0, 8.5)",              10,   8.0, 8.5, True)
    check_errors("SNF too low (10, 3.5, 6.5)",               10,   3.5, 6.5, True)
    check_errors("SNF too high (10, 3.5, 10.0)",             10,   3.5,10.0, True)
    check_errors("Valid entry (10, 3.5, 8.5) – no errors",   10,   3.5, 8.5, False)

    # ── Group 4: Five-entry hand-calculated total ──────────────────────────────
    print("\n[4] Five-entry batch – hand-calculated total")
    #   F001: 10 × 30.00 = 300.00
    #   F002: 8.5 × 33.40 = 283.90
    #   F003: 12 × 27.80 = 333.60
    #   F004: 9 × 31.60 = 284.40   (fat=3.8 → +3 steps; snf=8.6 → +1 step)
    #   F005: 7 × 32.20 = 225.40   (fat=4.0 → +5 steps; snf=8.5 → 0 steps)
    batch = [
        (10.0, 3.5, 8.5),
        ( 8.5, 4.2, 8.7),
        (12.0, 3.1, 8.3),
        ( 9.0, 3.8, 8.6),
        ( 7.0, 4.0, 8.5),
    ]
    total = ten_day_total(batch)
    # rate(3.8,8.6)=30+3×0.4+1×0.3=31.90; payout=9×31.90=287.10
    # rate(4.0,8.5)=30+5×0.4=32.00; payout=7×32.00=224.00
    expected_total = round(300.00 + 283.90 + 333.60 + 287.10 + 224.00, 2)
    check(f"5-entry total = Rs {expected_total}", total, expected_total)

    # ── Group 5: Invalid entries in batch are skipped ─────────────────────────
    print("\n[5] Batch with invalid entries (they are skipped)")
    mixed_batch = [
        (10.0,  3.5, 8.5),    # valid
        (-5.0,  3.5, 8.5),    # invalid: negative qty
        (10.0,  8.0, 8.5),    # invalid: fat too high
        ( 8.5,  4.2, 8.7),    # valid
    ]
    mixed_total = ten_day_total(mixed_batch)
    check("Skip 2 invalid, sum 2 valid = 583.90", mixed_total, 583.90)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print(f"  Tests passed: {PASS}   Failed: {FAIL}   Total: {PASS + FAIL}")
    print("=" * 70)
    if FAIL == 0:
        print("  All tests passed ✓")
    else:
        print("  *** Some tests FAILED – review the implementation ***")


if __name__ == "__main__":
    run_tests()
