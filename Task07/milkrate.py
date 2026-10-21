"""Rate card of the village milk co-operative (used as a module).

This module exposes the rate constants and the two core calculation
functions.  Import it from any script; the self-test table is printed
only when this file is run directly.
"""

# ─── Rate card constants ──────────────────────────────────────────────────────
BASE_RATE      = 30.00   # Rs per litre for 3.5 % fat and 8.5 % SNF
FAT_STEP_VALUE = 0.40    # Rs per litre for every 0.1 % fat above/below 3.5
SNF_STEP_VALUE = 0.30    # Rs per litre for every 0.1 % SNF above/below 8.5
BASE_FAT       = 3.5     # % – reference fat level
BASE_SNF       = 8.5     # % – reference SNF level
FAT_STEP_SIZE  = 0.1     # width of one fat step (%)
SNF_STEP_SIZE  = 0.1     # width of one SNF step (%)


def rate_per_litre(fat: float, snf: float) -> float:
    """
    Return the price per litre for given fat and SNF percentages.

    The deviation from the standard fat (3.5 %) and SNF (8.5 %) is
    expressed as a number of 0.1 % steps; round() is used instead of
    int() or math.floor() to avoid floating-point truncation errors
    (e.g., (4.2 - 3.5) / 0.1 evaluates to 7.000000000000001 in float).

    Parameters
    ----------
    fat : float  – fat percentage (e.g. 4.2)
    snf : float  – SNF percentage (e.g. 8.7)

    Returns
    -------
    float – rate in Rs/litre, rounded to 2 decimal places.

    Examples
    --------
    >>> rate_per_litre(3.5, 8.5)
    30.0
    >>> rate_per_litre(4.2, 8.7)
    33.4
    >>> rate_per_litre(3.1, 8.3)
    27.8
    """
    # TODO 1 – solution
    fat_steps = round((fat - BASE_FAT) / FAT_STEP_SIZE)
    snf_steps = round((snf - BASE_SNF) / SNF_STEP_SIZE)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return round(rate, 2)


def payout(litres: float, fat: float, snf: float) -> float:
    """
    Return the amount payable to the farmer for one delivery.

    Parameters
    ----------
    litres : float  – quantity in litres
    fat    : float  – fat percentage
    snf    : float  – SNF percentage

    Returns
    -------
    float – amount in Rs, rounded to 2 decimal places.

    Examples
    --------
    >>> payout(10, 3.5, 8.5)
    300.0
    >>> payout(8.5, 4.2, 8.7)
    283.9
    >>> payout(12, 3.1, 8.3)
    333.6
    """
    # TODO 2 – solution
    return round(litres * rate_per_litre(fat, snf), 2)


# ─────────────────────────────────────────────────────────────────────────────
# Self-test  –  runs ONLY when the module is executed directly
# (not when imported by another script)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("milkrate.py self-test")
    print("-" * 55)
    for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        rate, pay = rate_per_litre(fat, snf), payout(litres, fat, snf)
        print(f"{litres:5} L  fat {fat}  snf {snf}  rate {rate:6.2f}  pay {pay:8.2f}")
    print("-" * 55)
    print("When milkrate is imported, this block is skipped because")
    print("__name__ equals 'milkrate', not '__main__'.")
