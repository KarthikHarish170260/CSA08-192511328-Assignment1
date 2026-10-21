"""
Task 10 – Compare Expectations with Execution
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative

Measures float vs Decimal accuracy and timing for 300 / 6 000 / 150 000 payments.
Run with:  python Task10/task10_comparison.py
"""

import sys, os, time, random
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Task07'))
from milkrate import rate_per_litre, payout

# ─── Seed for reproducibility ────────────────────────────────────────────────
random.seed(42)

# ─────────────────────────────────────────────────────────────────────────────
# Generate a realistic set of n entries
# ─────────────────────────────────────────────────────────────────────────────

def generate_entries(n: int) -> list:
    """Generate n random (litres, fat, snf) entries within valid ranges."""
    entries = []
    for _ in range(n):
        litres = round(random.uniform(5.0, 20.0), 1)
        fat    = round(random.uniform(2.0, 7.0),  1)
        snf    = round(random.uniform(7.0, 9.5),  1)
        entries.append((litres, fat, snf))
    return entries


# ─────────────────────────────────────────────────────────────────────────────
# Float total
# ─────────────────────────────────────────────────────────────────────────────

def total_float(entries: list) -> float:
    """Sum payout() values as plain float."""
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Decimal total
# ─────────────────────────────────────────────────────────────────────────────

def total_decimal(entries: list) -> Decimal:
    """Sum payout() values using Decimal for exact paisa-level arithmetic."""
    total = Decimal("0.00")
    for litres, fat, snf in entries:
        # Convert the float payout to Decimal via string (avoids float error)
        total += Decimal(str(payout(litres, fat, snf)))
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ─────────────────────────────────────────────────────────────────────────────
# Rate-table cache (alternative concept for Task 10)
# ─────────────────────────────────────────────────────────────────────────────

def build_rate_table() -> dict:
    """
    Pre-compute rate for every (fat, snf) pair on the allowed grid.
    fat steps: 2.0, 2.1, ..., 7.0  (51 values)
    snf steps: 7.0, 7.1, ..., 9.5  (26 values)
    Total: 51 × 26 = 1 326 entries.
    Space: O(k) where k = 1 326.
    """
    table = {}
    fat_vals = [round(2.0 + i * 0.1, 1) for i in range(51)]
    snf_vals = [round(7.0 + i * 0.1, 1) for i in range(26)]
    for f in fat_vals:
        for s in snf_vals:
            table[(f, s)] = rate_per_litre(f, s)
    return table


def total_float_cached(entries: list, rate_table: dict) -> float:
    """Sum payments using a pre-built rate table (O(1) lookup per entry)."""
    total = 0.0
    for litres, fat, snf in entries:
        rate = rate_table.get((fat, snf), rate_per_litre(fat, snf))
        total += round(litres * rate, 2)
    return round(total, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Rounding experiment: round each payment vs round only the total
# ─────────────────────────────────────────────────────────────────────────────

def rounding_comparison(entries: list):
    """Show difference between per-payment rounding and end-total rounding."""
    per_payment_total = 0.0
    end_only_total    = 0.0

    for litres, fat, snf in entries:
        rate = rate_per_litre(fat, snf)
        per_payment_total += round(litres * rate, 2)
        end_only_total    += litres * rate

    return round(per_payment_total, 2), round(end_only_total, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Main comparison
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sizes = [300, 6_000, 150_000]

    print("=" * 78)
    print(f"{'n':>8}  {'float total':>14}  {'Decimal total':>14}  "
          f"{'Diff (paise)':>14}  {'float ms':>9}  {'Decimal ms':>10}")
    print("-" * 78)

    for n in sizes:
        entries = generate_entries(n)

        # Float timing
        t0 = time.perf_counter()
        f_total = total_float(entries)
        float_ms = (time.perf_counter() - t0) * 1000

        # Decimal timing
        t0 = time.perf_counter()
        d_total = total_decimal(entries)
        dec_ms = (time.perf_counter() - t0) * 1000

        diff_paise = abs(float(d_total) - f_total) * 100

        print(f"{n:>8}  {f_total:>14.2f}  {d_total:>14}  "
              f"{diff_paise:>14.4f}  {float_ms:>9.2f}  {dec_ms:>10.2f}")

    print("=" * 78)

    # Rounding comparison
    print("\n--- Rounding: per-payment vs end-total (n=6 000) ---")
    entries_6k = generate_entries(6_000)
    per_pay, end_only = rounding_comparison(entries_6k)
    print(f"  Per-payment rounding (correct bank method): Rs {per_pay:.2f}")
    print(f"  End-total rounding only                   : Rs {end_only:.2f}")
    diff = abs(per_pay - end_only)
    print(f"  Difference                                 : Rs {diff:.4f}  "
          f"({diff * 100:.2f} paise)")
    print(
        "\n  Conclusion: Round each payment individually (as the bank does).\n"
        "  Rounding only at the end accumulates sub-paisa errors across\n"
        "  thousands of entries, producing a total that differs from the\n"
        "  bank statement."
    )

    # Rate-table cache timing
    print("\n--- Rate-table cache vs recalculate (n=150 000) ---")
    entries_150k = generate_entries(150_000)

    t0 = time.perf_counter()
    rt = build_rate_table()
    build_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    cached = total_float_cached(entries_150k, rt)
    cache_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    direct = total_float(entries_150k)
    direct_ms = (time.perf_counter() - t0) * 1000

    print(f"  Rate table built in {build_ms:.2f} ms  ({len(rt)} entries)")
    print(f"  Cached lookup  (150 000 entries): {cache_ms:.2f} ms   total=Rs {cached:.2f}")
    print(f"  Direct recalc  (150 000 entries): {direct_ms:.2f} ms   total=Rs {direct:.2f}")
    print(
        "\n  The cache is worth it only when the same (fat, snf) pair\n"
        "  appears many times and rate_per_litre() is expensive.\n"
        "  For this problem the function is O(1) arithmetic, so the\n"
        "  difference is small.  Extra space: O(k) = O(1 326 pairs)."
    )
