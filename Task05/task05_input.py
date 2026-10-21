"""
Task 5 – Read Input and Convert Types
CSA0807 Python Programming Assignment 1
Ksheera Village Milk Co-operative
"""

# ─── Constants ────────────────────────────────────────────────────────────────
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 7.0, 9.5
QTY_MIN          = 0.0

# ─────────────────────────────────────────────────────────────────────────────
# Helper: safe float conversion with string-method pre-check (Approach A)
# ─────────────────────────────────────────────────────────────────────────────

def is_valid_number(text: str) -> bool:
    """
    Return True if 'text' looks like a valid non-negative decimal number.

    Strategy (string-method approach):
    - Strip leading/trailing whitespace.
    - Allow exactly one optional decimal point.
    - All remaining characters must be digits.
    This rejects "8,5" (comma), "eight" (letters), "" (empty).
    """
    text = text.strip()
    if not text:
        return False
    # Remove one optional leading minus sign (negative quantities rejected later)
    if text.startswith("-"):
        text = text[1:]
        if not text:
            return False
    parts = text.split(".")
    if len(parts) > 2:          # more than one dot → invalid
        return False
    return all(part.isdigit() for part in parts if part)   # every part is digits


def read_float(prompt: str, lo: float = None, hi: float = None) -> float:
    """
    Prompt the clerk for a number.  Validate with is_valid_number() before
    converting.  If lo/hi are supplied, also range-check the value.
    Returns the converted float.
    """
    while True:
        raw = input(prompt)
        if not is_valid_number(raw):
            print(f"  ✗ '{raw}' is not a valid number.  "
                  f"Use digits and a decimal point (e.g. 8.5).")
            continue
        value = float(raw.strip())
        if lo is not None and value < lo:
            print(f"  ✗ Value {value} is below the minimum ({lo}).")
            continue
        if hi is not None and value > hi:
            print(f"  ✗ Value {value} is above the maximum ({hi}).")
            continue
        return value


# ─────────────────────────────────────────────────────────────────────────────
# Alternative approach B: try/except ValueError
# ─────────────────────────────────────────────────────────────────────────────

def read_float_try(prompt: str, lo: float = None, hi: float = None) -> float:
    """
    Same contract as read_float(), but uses try/except ValueError.
    Handles "8,5" → float("8,5") raises ValueError → caught cleanly.
    Handles " 8.5 " → float(" 8.5 ") succeeds (float() strips whitespace).
    Handles "eight"  → ValueError → caught.
    """
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
        except ValueError:
            print(f"  ✗ '{raw}' cannot be converted to a number.")
            continue
        if lo is not None and value < lo:
            print(f"  ✗ Value {value} is below the minimum ({lo}).")
            continue
        if hi is not None and value > hi:
            print(f"  ✗ Value {value} is above the maximum ({hi}).")
            continue
        return value


# ─────────────────────────────────────────────────────────────────────────────
# Demonstration: show what each approach does with tricky inputs
# ─────────────────────────────────────────────────────────────────────────────

def demo_validation():
    """Show how is_valid_number handles edge-case strings."""
    print("=" * 60)
    print("SECTION 1 – is_valid_number() demo")
    print("=" * 60)
    test_cases = ["8.5", " 8.5 ", "8,5", "eight", "", "-3.0", "3.5.5", "0"]
    for s in test_cases:
        result = is_valid_number(s)
        print(f"  is_valid_number({s!r:12}) → {result}")

    print("\n  Note: ' 8.5 ' (with spaces) returns True because we strip first.\n"
          "  '8,5' returns False – comma is not a valid decimal separator.\n"
          "  try/except would also handle ' 8.5 ' (float() strips whitespace)\n"
          "  but would wrongly accept '1e3' (scientific notation).")


# ─────────────────────────────────────────────────────────────────────────────
# Formatted output using f-strings
# ─────────────────────────────────────────────────────────────────────────────

def print_payment_table(entries):
    """
    Print a neatly aligned payment table.

    F-string format specs used:
      {farmer_id:<8}   – left-align in an 8-character field
      {litres:6.1f}    – 6 wide, 1 decimal place
      {fat:5.2f}       – 5 wide, 2 decimal places
      {amount:8.2f}    – 8 wide, 2 decimal places (paisa precision)
    """
    BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = 30.00, 0.40, 0.30

    header = f"{'FarmerID':<8} {'Litres':>6} {'Fat%':>5} {'SNF%':>5} {'Rate':>7} {'Amount':>9}"
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for farmer_id, litres, fat, snf in entries:
        fat_steps = round((fat - 3.5) / 0.1)
        snf_steps = round((snf - 8.5) / 0.1)
        rate   = round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
        amount = round(litres * rate, 2)
        print(f"{farmer_id:<8} {litres:6.1f} {fat:5.2f} {snf:5.2f} {rate:7.2f} {amount:9.2f}")

    print("=" * len(header))


# ─────────────────────────────────────────────────────────────────────────────
# Main – run demo, then interactive entry if in script mode
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo_validation()

    # Sample entries to show formatted output without needing keyboard input
    sample_entries = [
        ("F001", 10.0, 3.5, 8.5),
        ("F002",  8.5, 4.2, 8.7),
        ("F003", 12.0, 3.1, 8.3),
        ("F004",  5.0, 2.0, 7.0),  # boundary low
        ("F005", 15.0, 7.0, 9.5),  # boundary high
    ]
    print_payment_table(sample_entries)

    # Interactive entry (comment out if running non-interactively)
    print("\n" + "=" * 60)
    print("Interactive Entry (Approach A – string method pre-check)")
    print("=" * 60)
    farmer_id = input("Farmer ID       : ").strip() or "F999"
    litres    = read_float("Quantity (litres): ", lo=0.001)
    fat       = read_float("Fat %            : ", lo=FAT_MIN, hi=FAT_MAX)
    snf       = read_float("SNF %            : ", lo=SNF_MIN, hi=SNF_MAX)
    print_payment_table([(farmer_id, litres, fat, snf)])
