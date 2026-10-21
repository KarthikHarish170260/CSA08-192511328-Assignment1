# Task 11 – Recommend and Defend the Final Design
# CSA0807 Python Programming Assignment 1
"""
This file prints the recommendation and design rationale.
Evidence is drawn from Task 10 measurements.
"""

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║       TASK 11 – Final Design Recommendation                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

RECOMMENDATION
══════════════

Use INTEGER PAISE internally + Decimal for totalling + named constants in a
separate milkrate.py module.

1. TYPES AND ROUNDING RULE
   ─────────────────────────
   • Each per-delivery payout is rounded to the nearest paisa (2 decimal
     places) INDIVIDUALLY, then summed.  This matches how the bank credits
     each transaction.
   • round() alone (on float) is acceptable for a single payment because the
     error is < 0.005.  For 150,000-entry district-union scale, use
     Decimal(str(amount)) summation to prevent drift.

   Evidence (Task 10):
     n=300     Decimal vs float diff ≈ 0.00 paise  (well within tolerance)
     n=6 000   diff ≈ 0.00–0.03 paise
     n=150 000 diff can reach 0.6 paise → use Decimal at district scale

   Verdict: float is fine for one collection centre (300 farmers × 20 entries
            = 6 000 records per cycle).  Decimal is required at 150 000 scale.

2. RATE REVISION PROCEDURE
   ─────────────────────────
   • All rates live in ONE file: milkrate.py (BASE_RATE, FAT_STEP_VALUE, etc.)
   • To revise: change the constant, re-run Task 9 tests, push the commit.
   • Every script that imports milkrate automatically picks up the new rate.
   • O(1) change locations — impossible to miss one file.

3. LIMITATIONS
   ─────────────
   • No database: data lives only in memory during a run; power loss loses it.
   • No multi-user access: two clerks cannot enter data simultaneously.
   • No audit trail: rejected entries are printed but not logged to a file.
   • No GUI: the clerks must type entries; a barcode/analyser interface would
     need a hardware driver layer.
   • Season detection is manual: the caller must pass season="peak".

4. SCALABILITY TO DISTRICT-UNION SCALE (150,000 FARMERS)
   ──────────────────────────────────────────────────────
   • The algorithm is O(n) time; it scales linearly and can process 150,000
     records in < 2 seconds on a modern laptop (measured in Task 10).
   • Memory: O(n) if all entries are stored, O(1) if a running total is used.
     At district scale use the running-total approach.
   • For 150,000 farmers, a relational database (SQLite → PostgreSQL) should
     replace in-memory lists; milkrate.py still provides the rate functions.

5. COMPARISON WITH ALTERNATIVES
   ──────────────────────────────
   • JSON rate file: eliminates code edits for rate revisions, but adds
     file-I/O risk and requires validation of the file contents.
     Recommended for production systems; acceptable overhead ≈ 1 ms at startup.
   • Rate-table cache: O(1) lookup per entry vs O(1) arithmetic per entry;
     difference is negligible for < 10 ms total.  Not worth the added
     complexity at collection-centre scale.

FINAL VERDICT
═════════════
  Design: milkrate.py module + round() per payment + Decimal for totals
          at district scale.
  Rounding: per-payment (matches bank).
  Constants: named UPPER_CASE constants in milkrate.py.
  This design is correct, readable, maintainable, and scales to district level
  with the running-total variant.
""")
