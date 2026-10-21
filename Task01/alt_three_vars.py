"""
CSA0807 - Assignment 1 - Task 1 (Alternative Concept and Complexity Analysis)

Compares two ways of holding the entries of n farmers:

  Design A (chosen)      : one tuple (litres, fat, snf) per entry, all kept in a list
  Design B (alternative) : three separate variables per entry: litres1, fat1, snf1, ...

Design B cannot be written with a loop, so this program GENERATES the Python
source that a clerk would otherwise have to type, then compiles and runs it.
That lets us measure source size, compile time, run time, peak memory and the
cost of fetching "farmer k" in both designs.

Run:
    python Task01/alt_three_vars.py            # measurements table
    python Task01/alt_three_vars.py --write    # also writes the 300-farmer
                                               # Design B program to disk
"""

import random
import sys
import time
import tracemalloc
from decimal import Decimal, ROUND_HALF_UP

# ---------------------------------------------------------------- constants
BASE_RATE = Decimal("30.00")   # Rs per litre at standard quality
STD_FAT = Decimal("3.5")       # standard fat %
STD_SNF = Decimal("8.5")       # standard SNF %
STEP = Decimal("0.1")          # one adjustment step, in % points
FAT_ADJ = Decimal("0.40")      # Rs per litre per 0.1 % fat
SNF_ADJ = Decimal("0.30")      # Rs per litre per 0.1 % SNF
PAISA = Decimal("0.01")        # smallest money unit

SIZES = (300, 1000, 3000, 6000)    # 1 centre ... 1 block (and in between)
REPEATS = 3                        # timings: best of 3
SEED = 2025                        # same data on every run


# ------------------------------------------------------------ shared logic
def rate_per_litre(fat, snf):
    """Rate in Rs per litre for the given fat % and SNF %."""
    return (BASE_RATE
            + (fat - STD_FAT) / STEP * FAT_ADJ
            + (snf - STD_SNF) / STEP * SNF_ADJ)


def amount(litres, fat, snf):
    """Payment for one entry, rounded half-up to the paisa."""
    return (litres * rate_per_litre(fat, snf)).quantize(PAISA, rounding=ROUND_HALF_UP)


def make_entries(n):
    """n valid entries as (litres, fat, snf) Decimals (fat 2.0-7.0, SNF 7.0-10.0)."""
    rng = random.Random(SEED)
    entries = []
    for _ in range(n):
        litres = Decimal(rng.randint(10, 500)) / 10      # 1.0 - 50.0 L
        fat = Decimal(rng.randint(20, 70)) / 10          # 2.0 - 7.0 %
        snf = Decimal(rng.randint(70, 100)) / 10         # 7.0 - 10.0 %
        entries.append((litres, fat, snf))
    return entries


# ------------------------------------------- Design A: one tuple per entry
def total_tuples(entries):
    total = Decimal("0.00")
    for litres, fat, snf in entries:
        total += amount(litres, fat, snf)
    return total


def fetch_all_tuples(entries):
    """Fetch entry k for k = 1..n by position: O(1) each."""
    n = len(entries)
    checksum = Decimal("0")
    for k in range(1, n + 1):
        litres, _fat, _snf = entries[k - 1]
        checksum += litres
    return checksum


# ------------------------- Design B: separate variables, generated source
def build_three_var_source(entries):
    """Source of the straight-line program a clerk would have to type."""
    n = len(entries)
    lines = []
    for i, (litres, fat, snf) in enumerate(entries, 1):
        lines.append(f"litres{i} = Decimal('{litres}')")
        lines.append(f"fat{i} = Decimal('{fat}')")
        lines.append(f"snf{i} = Decimal('{snf}')")
    lines.append("total = Decimal('0.00')")
    for i in range(1, n + 1):
        lines.append(f"total += amount(litres{i}, fat{i}, snf{i})")
    # fetching 'farmer k' needs one test per variable group (no indexing possible)
    lines.append("def fetch(k):")
    for i in range(1, n + 1):
        lines.append(f"    if k == {i}: return litres{i}, fat{i}, snf{i}")
    lines.append("checksum = Decimal('0')")
    lines.append(f"for k in range(1, {n} + 1):")
    lines.append("    checksum += fetch(k)[0]")
    return "\n".join(lines) + "\n"


def run_three_var(source):
    """Compile and execute Design B source; return (total, checksum)."""
    namespace = {"Decimal": Decimal, "amount": amount}
    exec(compile(source, "<three_vars>", "exec"), namespace)
    return namespace["total"], namespace["checksum"]


# ----------------------------------------------------------- measurements
def best_time(func, *args):
    best = None
    for _ in range(REPEATS):
        start = time.perf_counter()
        func(*args)
        elapsed = time.perf_counter() - start
        best = elapsed if best is None or elapsed < best else best
    return best


def peak_memory(func, *args):
    tracemalloc.start()
    func(*args)
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def build_and_total_tuples(n):
    """Design A including the memory needed to hold the n entries themselves."""
    return total_tuples(make_entries(n))


def measure(n):
    entries = make_entries(n)
    source = build_three_var_source(entries)

    total_a = total_tuples(entries)
    total_b, _ = run_three_var(source)
    if total_a != total_b:
        raise SystemExit(f"MISMATCH at n={n}: {total_a} vs {total_b}")

    return {
        "n": n,
        "total": total_a,
        "lines_a": 1 + 4,                         # the loop program is constant size
        "lines_b": source.count("\n"),
        "bytes_b": len(source.encode()),
        "time_a": best_time(total_tuples, entries),
        "time_b": best_time(run_three_var, source),   # compile + run
        "mem_a": peak_memory(build_and_total_tuples, n),   # data + result
        "mem_b": peak_memory(run_three_var, source),
    }


def main():
    print(f"Python {sys.version.split()[0]} - best of {REPEATS} runs, seed {SEED}\n")
    print("| n | total (Rs) | code lines A | code lines B | source B (KB) "
          "| time A (ms) | time B (ms) | peak mem A (KB) | peak mem B (KB) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for n in SIZES:
        r = measure(n)
        print(f"| {r['n']} | {r['total']} | {r['lines_a']} | {r['lines_b']} "
              f"| {r['bytes_b'] / 1024:.0f} | {r['time_a'] * 1000:.2f} "
              f"| {r['time_b'] * 1000:.2f} | {r['mem_a'] / 1024:.0f} "
              f"| {r['mem_b'] / 1024:.0f} |")

    # fetch-by-position cost, measured separately: O(1) vs O(n) per lookup
    print("\nFetch farmer k for every k = 1..n (time B includes the generated "
          "if-chain):")
    for n in SIZES:
        entries = make_entries(n)
        source = build_three_var_source(entries)
        namespace = {"Decimal": Decimal, "amount": amount}
        exec(compile(source, "<three_vars>", "exec"), namespace)
        fetch = namespace["fetch"]

        def fetch_all_b():
            for k in range(1, n + 1):
                fetch(k)

        print(f"  n={n:>5}: A {best_time(fetch_all_tuples, entries) * 1000:8.3f} ms"
              f"   B {best_time(fetch_all_b) * 1000:10.3f} ms")

    if "--write" in sys.argv:
        path = "three_vars_300_farmers_generated.py"
        entries = make_entries(300)
        header = ("# GENERATED: Design B for 300 farmers (900 data variables).\n"
                  "from decimal import Decimal\n"
                  "from alt_three_vars import amount\n\n")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header + build_three_var_source(entries))
        print(f"\nWrote {path}")


if __name__ == "__main__":
    main()