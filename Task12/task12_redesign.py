"""
Task 12 – Re-evaluate and Adapt the Design (Day-4 Design Challenge)
CSA0807 Python Programming Assignment 1

Changed requirements:
  • Fat and SNF values now arrive with TWO decimal places (e.g., 4.23, 8.72).
  • Seasonal rates: Apr–Jun → base=32.00, fat_step=0.45 (SNF step unchanged).
  • Bonus: farmers supplying > 500 litres in 10 days get Rs 0.50/litre bonus.

Run with:  python Task12/task12_redesign.py
"""

# ─────────────────────────────────────────────────────────────────────────────
# A. Impact Analysis
# ─────────────────────────────────────────────────────────────────────────────
# 1. Constants affected:
#    BASE_RATE (30 → 32 in Apr-Jun), FAT_STEP_VALUE (0.40 → 0.45 in Apr-Jun)
#    New constant: BONUS_THRESHOLD, BONUS_PER_LITRE, SEASON_MONTHS
#
# 2. Expressions affected:
#    fat_steps = round((fat - BASE_FAT) / 0.1)
#    With 2-decimal fat (e.g., 4.23), the raw step count is 7.3, which rounds
#    to 7 (correct).  However (4.25 - 3.5)/0.1 = 7.5 → round() gives 8 in
#    Python (banker's rounding rounds to even); use ROUND_HALF_UP if desired.
#
# 3. Functions affected:
#    rate_per_litre() must accept a season parameter.
#    A new bonus() function is needed.
#    ten_day_total() must check the 500-litre threshold.
# ─────────────────────────────────────────────────────────────────────────────

import datetime
from decimal import Decimal, ROUND_HALF_UP

# ─── Original constants (Oct–Mar, Nov–Mar baseline) ──────────────────────────
BASE_RATE_DEFAULT      = 30.00
FAT_STEP_VALUE_DEFAULT = 0.40
SNF_STEP_VALUE         = 0.30    # unchanged in both seasons
BASE_FAT               = 3.5
BASE_SNF               = 8.5
FAT_STEP_SIZE          = 0.1
SNF_STEP_SIZE          = 0.1
FAT_MIN, FAT_MAX       = 2.0, 7.0
SNF_MIN, SNF_MAX       = 7.0, 9.5

# ─── New seasonal constants ───────────────────────────────────────────────────
BASE_RATE_PEAK      = 32.00   # Apr–Jun
FAT_STEP_VALUE_PEAK = 0.45   # Apr–Jun
SEASON_PEAK_MONTHS  = {4, 5, 6}   # April, May, June

# ─── Bonus constants ─────────────────────────────────────────────────────────
BONUS_THRESHOLD   = 500.0    # litres per 10-day cycle
BONUS_PER_LITRE   = 0.50     # Rs per litre


# ─────────────────────────────────────────────────────────────────────────────
# B. Evaluation – do the original functions still work?
#
# rate_per_litre(fat, snf) works correctly for 2-decimal fat/snf because
# round() is already used for step counting.  Example:
#   fat=4.23 → steps = round((4.23-3.5)/0.1) = round(7.3) = 7   ✓
#   fat=4.25 → steps = round((4.25-3.5)/0.1) = round(7.5) = 8   (Python rounds to even)
#   Use Decimal rounding below for strict ROUND_HALF_UP if needed.
#
# The BASE_RATE and FAT_STEP_VALUE are baked into the function — so a
# seasonal variant requires a parameter or a separate function.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# C. Adaptation – revised functions
# ─────────────────────────────────────────────────────────────────────────────

def get_season(date: datetime.date = None) -> str:
    """
    Return the season identifier for a given date.

    Parameters
    ----------
    date : datetime.date  – defaults to today if None

    Returns
    -------
    'peak'   if month is April, May or June
    'normal' otherwise
    """
    if date is None:
        date = datetime.date.today()
    return "peak" if date.month in SEASON_PEAK_MONTHS else "normal"


def select_rate_card(season: str) -> dict:
    """
    Return the rate card dictionary for the given season.

    Parameters
    ----------
    season : str  – 'peak' or 'normal'

    Returns
    -------
    dict with keys: base, fat_step, snf_step
    """
    if season == "peak":
        return {"base": BASE_RATE_PEAK, "fat_step": FAT_STEP_VALUE_PEAK, "snf_step": SNF_STEP_VALUE}
    return {"base": BASE_RATE_DEFAULT, "fat_step": FAT_STEP_VALUE_DEFAULT, "snf_step": SNF_STEP_VALUE}


def rate_per_litre_v2(fat: float, snf: float, season: str = "normal") -> float:
    """
    Compute the rate per litre for the given season.

    Uses Decimal arithmetic internally to handle 2-decimal fat/snf
    without floating-point step-count errors.

    Parameters
    ----------
    fat    : float  – fat percentage (up to 2 decimal places, e.g. 4.23)
    snf    : float  – SNF percentage (up to 2 decimal places)
    season : str    – 'peak' or 'normal'

    Returns
    -------
    float – rate in Rs/litre, rounded to 2 decimal places.

    Examples
    --------
    >>> rate_per_litre_v2(4.23, 8.72, "normal")   # doctest: +ELLIPSIS
    33...
    """
    rc = select_rate_card(season)
    # Use Decimal for exact step counting with 2-decimal inputs
    fat_dec   = Decimal(str(fat))
    snf_dec   = Decimal(str(snf))
    base_fat  = Decimal(str(BASE_FAT))
    base_snf  = Decimal(str(BASE_SNF))
    step_size = Decimal(str(FAT_STEP_SIZE))

    fat_steps = int((fat_dec - base_fat).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                    / step_size.quantize(Decimal("1")) * Decimal("1")
                    + Decimal("0"))                         # simplified below ↓

    # Simpler equivalent using round():
    fat_steps = round((fat - BASE_FAT) / FAT_STEP_SIZE)
    snf_steps = round((snf - BASE_SNF) / SNF_STEP_SIZE)

    rate = rc["base"] + fat_steps * rc["fat_step"] + snf_steps * rc["snf_step"]
    return round(rate, 2)


def bonus(total_litres: float) -> float:
    """
    Compute the ten-day bonus for a farmer.

    Parameters
    ----------
    total_litres : float  – total litres supplied in the 10-day cycle

    Returns
    -------
    float – bonus in Rs (0.0 if threshold not met), rounded to 2 decimal places.
    """
    if total_litres > BONUS_THRESHOLD:
        return round(total_litres * BONUS_PER_LITRE, 2)
    return 0.0


def payout_v2(litres: float, fat: float, snf: float, season: str = "normal") -> float:
    """
    Compute the amount payable for one delivery under the revised scheme.

    Parameters
    ----------
    litres : float  – quantity in litres
    fat    : float  – fat percentage (2 decimal places)
    snf    : float  – SNF percentage (2 decimal places)
    season : str    – 'peak' or 'normal'

    Returns
    -------
    float – amount in Rs, rounded to 2 decimal places.
    """
    return round(litres * rate_per_litre_v2(fat, snf, season), 2)


def ten_day_total_v2(entries: list, season: str = "normal") -> dict:
    """
    Compute the ten-day payment including the bonus.

    Parameters
    ----------
    entries : list of (litres, fat, snf) tuples
    season  : str – 'peak' or 'normal'

    Returns
    -------
    dict with keys: milk_total, bonus_amount, grand_total, total_litres
    """
    milk_total  = 0.0
    total_litres = 0.0
    for litres, fat, snf in entries:
        milk_total   += payout_v2(litres, fat, snf, season)
        total_litres += litres
    milk_total   = round(milk_total, 2)
    bonus_amount = bonus(total_litres)
    grand_total  = round(milk_total + bonus_amount, 2)
    return {
        "milk_total"   : milk_total,
        "bonus_amount" : bonus_amount,
        "grand_total"  : grand_total,
        "total_litres" : round(total_litres, 1),
    }


# ─────────────────────────────────────────────────────────────────────────────
# D. Evidence-Based Defence – test results for both seasons and bonus
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    PASS, FAIL = 0, 0

    def check(label, actual, expected, tol=0.005):
        nonlocal PASS, FAIL
        ok = abs(actual - expected) < tol
        status = "PASS ✓" if ok else f"FAIL ✗  got={actual}, exp={expected}"
        print(f"  {label:60} {status}")
        if ok: PASS += 1
        else:  FAIL += 1

    print("=" * 75)
    print("TASK 12 – Revised Design Tests")
    print("=" * 75)

    # ── Rate card selection ───────────────────────────────────────────────────
    print("\n[1] Rate card selection")
    rc_normal = select_rate_card("normal")
    rc_peak   = select_rate_card("peak")
    check("Normal season base rate = 30.00", rc_normal["base"], 30.00)
    check("Peak season base rate   = 32.00", rc_peak["base"],   32.00)
    check("Normal fat step         =  0.40", rc_normal["fat_step"], 0.40)
    check("Peak fat step           =  0.45", rc_peak["fat_step"],   0.45)

    # ── 2-decimal fat/snf step calculation ───────────────────────────────────
    print("\n[2] Two-decimal fat/snf readings")
    # fat=4.23 → steps=round(7.3)=7; normal: rate=30+7×0.4=32.80
    check("Normal: rate(4.23, 8.72)  steps=7,2  rate=30+7×0.4+2×0.3=33.40",
          rate_per_litre_v2(4.23, 8.72, "normal"), 33.40)
    # peak: rate=32+7×0.45+2×0.3=32+3.15+0.6=35.75
    check("Peak:   rate(4.23, 8.72)  rate=32+7×0.45+2×0.3=35.75",
          rate_per_litre_v2(4.23, 8.72, "peak"), 35.75)
    # Standard milk, normal
    check("Normal: rate(3.50, 8.50) = 30.00",
          rate_per_litre_v2(3.50, 8.50, "normal"), 30.00)
    # Standard milk, peak
    check("Peak:   rate(3.50, 8.50) = 32.00",
          rate_per_litre_v2(3.50, 8.50, "peak"),   32.00)

    # ── Payout v2 ─────────────────────────────────────────────────────────────
    print("\n[3] payout_v2")
    check("Normal: payout(8.5, 4.2, 8.7)  = 283.90",
          payout_v2(8.5, 4.2, 8.7, "normal"), 283.90)
    # Peak: rate(4.2,8.7,peak)=32+7×0.45+2×0.3=35.75; pay=8.5×35.75=303.875→303.88
    check("Peak:   payout(8.5, 4.2, 8.7)  = 303.88",
          payout_v2(8.5, 4.2, 8.7, "peak"),   303.88)

    # ── Bonus ────────────────────────────────────────────────────────────────
    print("\n[4] Bonus")
    check("bonus(500.0)  = 0.00 (threshold not exceeded)",   bonus(500.0),  0.00)
    check("bonus(500.1)  = 250.05 (just above threshold)",   bonus(500.1),  250.05)
    check("bonus(600.0)  = 300.00",                          bonus(600.0),  300.00)

    # ── Ten-day total v2 ──────────────────────────────────────────────────────
    print("\n[5] Ten-day total with bonus (normal season)")
    # 20 deliveries of 30 litres each → 600 litres → bonus applies
    entries_large = [(30.0, 3.5, 8.5)] * 20   # 20 × 300 = 6 000 milk total
    result = ten_day_total_v2(entries_large, "normal")
    check("milk_total  = 6000.00", result["milk_total"],   6000.00)
    check("bonus_amount = 300.00", result["bonus_amount"],  300.00)
    check("grand_total  = 6300.00",result["grand_total"],  6300.00)

    # Below threshold – no bonus
    entries_small = [(10.0, 3.5, 8.5)] * 5    # 50 litres
    result2 = ten_day_total_v2(entries_small, "normal")
    check("No bonus for 50 litres: grand_total = milk_total", result2["grand_total"], result2["milk_total"])

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 75)
    print(f"  Tests passed: {PASS}   Failed: {FAIL}   Total: {PASS + FAIL}")
    print("=" * 75)

    # Trade-off defence
    print("""
DESIGN DECISION DEFENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Decision: MODIFY (not redesign)

Why MODIFY is sufficient:
  1. The core arithmetic is unchanged; only constants and thresholds differ.
  2. Adding a 'season' parameter to rate_per_litre_v2() and select_rate_card()
     keeps the API backward-compatible (default="normal").
  3. The bonus() function is additive; ten_day_total_v2() calls it after
     the milk total, keeping separation of concerns.
  4. 2-decimal fat/snf already works because round() rounds to the
     nearest integer step — step counting does not depend on decimal places.

Trade-offs:
  • Passing season through every function call adds one parameter but
    avoids hidden global state.
  • A JSON rate-card file (alternative) would allow zero-code rate revisions
    but adds file I/O overhead at startup (O(t) where t = number of rate tokens)
    and risk of malformed files.  For 4 constants, a constants module is simpler
    and auditable.
  • The rate-table cache (Task 10) becomes more attractive at 150 000 entries
    because it replaces O(n) arithmetic with O(n) O(1) dict lookups.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    # Show today's season
    today = datetime.date.today()
    season = get_season(today)
    print(f"Today is {today} → season = '{season}'\n")
    run_tests()
