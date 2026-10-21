"""
Task 6 – Organise the Logic into Functions
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative
"""

# ─── Module-level constants (read inside functions, never reassigned) ──────────
BASE_RATE      = 30.00   # Rs/litre for standard 3.5 % fat, 8.5 % SNF
BASE_FAT       = 3.5     # % reference fat
BASE_SNF       = 8.5     # % reference SNF
FAT_STEP_VALUE = 0.40    # Rs per 0.1 % fat deviation
SNF_STEP_VALUE = 0.30    # Rs per 0.1 % SNF deviation
FAT_STEP_SIZE  = 0.1     # width of one fat step in %
SNF_STEP_SIZE  = 0.1     # width of one SNF step in %
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 7.0, 9.5


# ─────────────────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────────────────

def validate_entry(litres: float, fat: float, snf: float) -> list:
    """
    Validate a single farmer entry.

    Parameters
    ----------
    litres : float  – quantity of milk in litres (must be > 0)
    fat    : float  – fat percentage
    snf    : float  – SNF percentage

    Returns
    -------
    list of str – list of error messages; empty list means the entry is valid.
    """
    errors = []
    if litres <= 0:
        errors.append(f"Quantity must be positive (got {litres}).")
    if not (FAT_MIN <= fat <= FAT_MAX):
        errors.append(f"Fat% {fat} out of range [{FAT_MIN}, {FAT_MAX}].")
    if not (SNF_MIN <= snf <= SNF_MAX):
        errors.append(f"SNF% {snf} out of range [{SNF_MIN}, {SNF_MAX}].")
    return errors


def rate_per_litre(fat: float, snf: float) -> float:
    """
    Compute the price per litre for a given fat and SNF reading.

    The number of 0.1 % fat (and SNF) steps from the standard is found with
    round() to avoid floating-point truncation errors (e.g. 7.000000000000001
    instead of 7).  Each step adds or subtracts the corresponding step value.

    Parameters
    ----------
    fat : float  – fat percentage (e.g. 4.2)
    snf : float  – SNF percentage (e.g. 8.7)

    Returns
    -------
    float – rate in Rs per litre, rounded to 2 decimal places.
    """
    fat_steps = round((fat - BASE_FAT) / FAT_STEP_SIZE)
    snf_steps = round((snf - BASE_SNF) / SNF_STEP_SIZE)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return round(rate, 2)


def payout(litres: float, fat: float, snf: float) -> float:
    """
    Compute the amount payable for a single delivery.

    Parameters
    ----------
    litres : float  – quantity in litres
    fat    : float  – fat percentage
    snf    : float  – SNF percentage

    Returns
    -------
    float – amount in Rs, rounded to 2 decimal places (nearest paisa).
    """
    return round(litres * rate_per_litre(fat, snf), 2)


def ten_day_total(entries: list) -> float:
    """
    Compute the ten-day payment total for one farmer.

    Each entry in 'entries' is a tuple (litres, fat, snf).
    Individual payouts are summed; the total is returned as a float
    rounded to 2 decimal places.

    Parameters
    ----------
    entries : list of (float, float, float) tuples

    Returns
    -------
    float – total amount in Rs, rounded to 2 decimal places.
    """
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)


def print_receipt(farmer_id: str, entries: list) -> None:
    """
    Print a formatted receipt for one farmer covering one ten-day cycle.

    Parameters
    ----------
    farmer_id : str  – unique identifier for the farmer
    entries   : list of (litres, fat, snf) tuples, one per delivery

    Returns
    -------
    None  (prints directly; does NOT return the total)
    """
    header = f"{'#':>3} {'Litres':>7} {'Fat%':>5} {'SNF%':>5} {'Rate':>7} {'Amount':>9}"
    print(f"\n  Farmer: {farmer_id}")
    print("  " + "─" * len(header))
    print("  " + header)
    print("  " + "─" * len(header))

    for i, (litres, fat, snf) in enumerate(entries, 1):
        rate   = rate_per_litre(fat, snf)
        amount = payout(litres, fat, snf)
        print(f"  {i:>3} {litres:>7.1f} {fat:>5.2f} {snf:>5.2f} {rate:>7.2f} {amount:>9.2f}")

    total = ten_day_total(entries)
    print("  " + "─" * len(header))
    print(f"  {'10-day total':>{len(header)-10}} {total:>9.2f}")
    print("  " + "─" * len(header))


# ─────────────────────────────────────────────────────────────────────────────
# Scope demonstration
# ─────────────────────────────────────────────────────────────────────────────

def demo_scope():
    """
    Demonstrate local vs global names.

    BASE_RATE is a module-level name; it can be READ inside any function
    without a 'global' declaration.  Reassigning it (BASE_RATE = ...) inside
    a function would create a LOCAL variable that shadows the global one —
    it would NOT change the module constant.  We avoid this by convention.
    """
    # This reads the module-level BASE_RATE without 'global':
    local_base = BASE_RATE          # local variable; BASE_RATE unchanged
    print(f"\n  Inside demo_scope(): BASE_RATE = {BASE_RATE}  (read, not modified)")
    print(f"  local_base = {local_base}  (a local copy)")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("TASK 6 – Functions Demo")
    print("=" * 60)

    # Test rate_per_litre
    print("\nrate_per_litre tests:")
    for fat, snf, expected in [(3.5, 8.5, 30.00), (4.2, 8.7, 33.40), (3.1, 8.3, 27.80)]:
        r = rate_per_litre(fat, snf)
        status = "✓" if r == expected else "✗"
        print(f"  fat={fat}, snf={snf}  → Rs {r}  expected Rs {expected}  {status}")

    # Sample ten-day data for farmer F001
    farmer_entries = [
        (10.0, 3.5, 8.5),
        ( 8.5, 4.2, 8.7),
        (12.0, 3.1, 8.3),
        ( 9.0, 3.8, 8.6),
        (11.0, 4.0, 8.8),
    ]

    print_receipt("F001", farmer_entries)

    # Validation demo
    print("\nvalidate_entry tests:")
    for args in [(-1, 3.5, 8.5), (10, 8.0, 8.5), (10, 3.5, 5.0), (10, 3.5, 8.5)]:
        errs = validate_entry(*args)
        status = "VALID" if not errs else "INVALID: " + "; ".join(errs)
        print(f"  {args}  → {status}")

    demo_scope()

    # Alternative: lambda for a simple rate lookup (not recommended for full logic)
    print("\n--- Alternative: lambda expression ---")
    quick_rate = lambda fat, snf: round(
        BASE_RATE
        + round((fat - BASE_FAT) / 0.1) * FAT_STEP_VALUE
        + round((snf - BASE_SNF) / 0.1) * SNF_STEP_VALUE,
        2,
    )
    print(f"  quick_rate(4.2, 8.7) = {quick_rate(4.2, 8.7)}")
    print(
        "  Lambda: works for one-liners but cannot have a docstring,\n"
        "  multi-line logic, or meaningful name — reduces readability.\n"
        "  Function call overhead is O(1) and negligible for 150 000 entries."
    )
