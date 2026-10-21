# Task 1 – Understand the Problem and Identify the Data

**Course:** CSA0807 Python Programming – Assignment 1
**Name:** Karthik  **Register No:** 192511328

---

## 1. What the program must do

For every milk entry, price the milk from its fat % and SNF %, multiply by the
litres, and pay each farmer the total of all their entries over a ten-day cycle.
Every amount must be correct **to the paisa**, and the design must still work when
300 farmers become 6,000 (block) and 150,000 (district union).

## 2. Inputs and outputs

### Inputs (recorded by the clerk, per entry)

| Input | Meaning | Why it is needed |
|---|---|---|
| Farmer ID | Identifies who is paid | Entries are grouped by farmer for the ten-day total |
| Litres | Quantity delivered | Amount = litres × rate |
| Fat % | Fat content | Raises/lowers the rate by Rs 0.40 per 0.1 % from 3.5 % |
| SNF % | Solids-not-fat content | Raises/lowers the rate by Rs 0.30 per 0.1 % from 8.5 % |
| Shift | Morning or evening | Two collections a day; identifies the entry and lets a duplicate (same farmer, day, shift) be caught |

### Outputs

| Output | Computed from | Notes |
|---|---|---|
| Rate per litre | Fat, SNF and the rate constants | Same formula for every entry |
| Amount for the entry | Litres × rate per litre | Rounded to the paisa **once**, per entry |
| Ten-day total per farmer | Sum of that farmer's entry amounts | This is the figure compared with the bank statement |

## 3. Values that never change during a run – named constants

These are written **once**, with names, because the present program has the
rates typed in several places and a revision was applied only partly. One
definition means one place to revise.

| Constant | Value | Justification |
|---|---|---|
| `BASE_RATE` | 30.00 | Rate for standard milk |
| `STD_FAT` | 3.5 | Fat % at which the base rate applies |
| `STD_SNF` | 8.5 | SNF % at which the base rate applies |
| `STEP` | 0.1 | The size of one adjustment step, in % points |
| `FAT_ADJ` | 0.40 | Rs per litre per step of fat |
| `SNF_ADJ` | 0.30 | Rs per litre per step of SNF |
| `MIN_FAT`, `MAX_FAT` | 2.0, 7.0 | Valid fat range given in the problem |
| `MIN_SNF`, `MAX_SNF` | 7.0, 10.0 | **Assumed** (see §6): the sheet gives no SNF range |
| `MAX_LITRES` | 100 | **Assumed** upper limit for one entry; catches typing errors such as 3000 for 30.0 |
| `PAISA` | 0.01 | Smallest money unit; every amount is rounded to this |
| `DAYS_PER_CYCLE` | 10 | Payment period |
| `SHIFTS` | `"M"`, `"E"` | The only two valid shifts |

Rates are constants **for one run**, not for the life of the co-operative: seasonal
revisions will change them. That is why they must sit in one place (one module
or a file) rather than be scattered through the code.

## 4. Types of the values

| Kind | Values | Type chosen | Justification |
|---|---|---|---|
| **Text** | Farmer ID, shift | `str` | An ID such as `"F007"` or `"0042"` is a label: no arithmetic is done on it, and a leading zero must not be lost (an `int` would turn `0042` into `42`) |
| **Whole numbers** | Number of farmers *n*, days in the cycle (10), number of entries per farmer, number of steps away from standard (if counted as an integer) | `int` | These are counted, never fractional |
| **Fractional** | Litres, fat %, SNF %, rate per litre, amount, ten-day total | `Decimal` (not `float`) | See below |

### Why `Decimal`, not `float`

The complaint is totals that "differ from the bank statement by a few paise".
That is the typical symptom of binary floating point: `0.1` and `0.3` cannot be
stored exactly, so `0.1 + 0.2 == 0.3` is `False` in Python and the error accumulates
over many entries. `Decimal` stores `3.5`, `0.40`, `8.5` exactly and
`quantize(Decimal("0.01"), ROUND_HALF_UP)` gives a controlled, repeatable
rounding rule to the paisa. Its cost is speed (see the measurements below), which
is acceptable because only a few hundred to a few lakh multiplications are done
per cycle. Values must be created from **strings** (`Decimal("3.5")`); building
them from floats (`Decimal(3.5)` or `Decimal(0.1)`) copies the float's error.

## 5. Rules every correct payment must satisfy

| # | Rule | Reason |
|---|---|---|
| R1 | Litres must be a number greater than 0 and not above `MAX_LITRES` | A negative quantity would reduce a farmer's pay; 0 is not a delivery; a very large value is almost certainly a typing slip |
| R2 | Fat % must be between 2.0 and 7.0 **inclusive** | Given in the problem; the end values 2.0 and 7.0 are valid (using `<` instead of `<=` is a typical cause of "rejects valid entries") |
| R3 | SNF % must be between `MIN_SNF` and `MAX_SNF` inclusive | Same reason; range assumed |
| R4 | Shift must be exactly `"M"` or `"E"` | Prevents misrecorded or duplicate shifts |
| R5 | Farmer ID must be non-empty text | An entry without an owner cannot be paid |
| R6 | Fat, SNF and litres must be read as numbers; non-numeric input is rejected with a message, not a crash | Clerk typing errors are expected |
| R7 | Rate per litre = 30.00 + ((fat − 3.5) / 0.1) × 0.40 + ((snf − 8.5) / 0.1) × 0.30 | The pricing rule; the constants come from §3 |
| R8 | Entry amount = litres × rate, rounded half-up to the paisa **once** | Gives a fixed, repeatable result |
| R9 | Ten-day total = sum of the already-rounded entry amounts | The total must equal the sum of the amounts the farmer sees |
| R10 | No two entries share the same farmer, day and shift | A double entry would pay twice |

**Check on R7 with the allowed ranges:** the lowest possible rate is
30.00 − 15 × 0.40 − 15 × 0.30 = **Rs 19.50** (fat 2.0, SNF 7.0) and the highest is
30.00 + 35 × 0.40 + 15 × 0.30 = **Rs 48.50** (fat 7.0, SNF 10.0). With R1–R3 enforced
the rate is therefore never zero or negative.

## 6. Assumptions

1. **Fat and SNF are entered to one decimal place** (e.g. 3.5, 8.6). The formula
   works for more decimals (the analyser may give two) because `Decimal` divides
   by 0.1 exactly, so no change is needed when the analyser is installed.
2. **SNF range is 7.0–10.0 %.** The problem fixes only the fat range. This is my
   assumption; if the co-operative states another range, only `MIN_SNF` and
   `MAX_SNF` change.
3. **Maximum 100 L per entry.** The problem does not state a limit; this is a
   typing-error guard and is a single constant to change.
4. **Rounding rule:** round each entry half-up to the paisa, then add. If the bank
   rounds only the final total, results can differ by a few paise; this should be
   confirmed against the bank statement, and the choice is isolated in one function.
5. **A cycle has at most 20 entries per farmer** (10 days × 2 shifts).
6. **Each entry is one complete record.** Fat and SNF belong to the litres
   delivered in the same entry, so the three values travel together.
7. Money is in rupees with two decimal places; currency conversion is not needed.

---

# Alternative Concept and Complexity Analysis

## A. The two designs

**Design A (chosen):** one tuple per entry, all stored in one list.

```python
entries = [
    (Decimal("29.5"), Decimal("4.1"), Decimal("8.7")),
    (Decimal("18.0"), Decimal("3.4"), Decimal("8.5")),
    # ... one tuple per entry
]

total = Decimal("0.00")
for litres, fat, snf in entries:
    total += amount(litres, fat, snf)
```

**Design B (alternative):** three separate variables per entry.

```python
litres1 = Decimal("29.5");  fat1 = Decimal("4.1");  snf1 = Decimal("8.7")
litres2 = Decimal("18.0");  fat2 = Decimal("3.4");  snf2 = Decimal("8.5")
# ... 3 variables for every farmer: 900 variables for 300 farmers

total = Decimal("0.00")
total += amount(litres1, fat1, snf1)
total += amount(litres2, fat2, snf2)
# ... 300 separate lines, one per farmer
```

For 300 farmers, Design B needs **900 variable definitions + 300 `total +=`
lines** (about 1,500 lines with the lookup function used below). A loop cannot be
used, because `litres1`, `litres2`, ... are different *names*, not elements of one
structure that a loop variable can step through. Reading the input from a
keyboard or file would also need 300 separate input statements.

`alt_three_vars.py` generates this program (it is too long to type) and runs both
designs on identical data. **Both give identical totals at every size**, so the
comparison is purely about cost.

## B. Time and space analysis

Let *n* be the number of entries.

| Measure | Design A (list of tuples) | Design B (3 variables each) |
|---|---|---|
| Arithmetic to process all entries | O(n): one `amount()` call per entry | O(n): the same calls, written out one by one |
| Fetch entry *k* by position | **O(1)**: `entries[k-1]` | **O(n)**: no indexing exists; needs a chain of `if k == 1 ... if k == 2 ...` (a `globals()` trick would be O(1) but is fragile and no longer "separate variables") |
| Fetch every entry once | O(n) | **O(n²)** |
| Program size (lines of code) | **O(1)**: 5 lines for any *n* | **O(n)**: grows with every farmer |
| Compile time | O(1) | O(n) (the compiler must read the whole program) |
| Space for the data | O(n) | O(n) |
| Extra space | O(1) | O(n) code object, names and constants besides the data |
| Can *n* be decided while running? | Yes | **No**: *n* is fixed when the program is typed |

Key point: **the arithmetic is O(n) in both**. Every entry must be priced at
least once, so no design can do better. The designs differ in what happens around the
arithmetic: how the program is written, how entries are fetched, and what the
interpreter must hold.

## C. My measurements

Measured with `python Task01/alt_three_vars.py` (Python 3.12.3, best of 3,
same random data each run). Time B includes compiling and running the generated
program, because that is the true cost of Design B. Memory is the peak measured with
`tracemalloc`, including the data itself in both designs.

| n | total (Rs) | code lines A | code lines B | source B (KB) | time A (ms) | time B (ms) | peak mem A (KB) | peak mem B (KB) |
|---|---|---|---|---|---|---|---|---|
| 300 | 268217.24 | 5 | 1505 | 48 | 0.24 | 8.86 | 132 | 6222 |
| 1000 | 855639.56 | 5 | 5005 | 163 | 0.81 | 35.12 | 433 | 19585 |
| 3000 | 2619292.40 | 5 | 15005 | 511 | 2.41 | 144.66 | 1294 | 61717 |
| 6000 | 5163462.05 | 5 | 30005 | 1033 | 5.00 | 361.00 | 2586 | 123578 |

Fetching farmer *k* for every *k* = 1..n:

| n | Design A (ms) | Design B (ms) |
|---|---|---|
| 300 | 0.023 | 0.334 |
| 1000 | 0.074 | 3.837 |
| 3000 | 0.232 | 36.877 |
| 6000 | 0.500 | 148.396 |

**What the numbers show**

- **Design A is linear:** going from 300 to 6,000 entries (20×) raised its time from
  0.27 ms to 5.59 ms (about 21×) and its memory from 115 KB to 2,258 KB (about 20×);
  its code stayed 5 lines.
- **Design B's code and memory also grow linearly with *n*,** but from a much
  higher base: at n = 300 it needs 1,505 lines and about 5.9 MB, against 5 lines and
  about 115 KB. Its time grew about 40× for a 20× larger *n*: slightly worse than
  linear, which fits the compiler and memory management having more to do.
  Design B took about 40× longer than Design A at n = 300, and the gap widened to about 80× at n = 6,000.
- **Fetch by position separates them clearly.** For a 20× larger *n*, Design A
  rose about 24× (O(n) total for *n* O(1) lookups), while Design B rose about 530×,
  close to the 400× expected from O(n²).
- Extrapolating the trend to **150,000 farmers** (district union), Design B would
  be about 750,000 lines of source and roughly 3 GB of memory if growth stays linear
  (it grew slightly faster than linear here). I did not run that size; it
  is an extrapolation from the n = 6,000 row. Design A at that size would need only
  about 56 MB and still be the same 5 lines.

## D. Why the second design scales and the first does not

1. **Code length must not depend on data size.** In Design B each new farmer means
   more source code, which someone has to type, check and debug. In Design A a new
   farmer is one more tuple in the data.
2. **A loop needs something to step through.** A list gives a position
   (`entries[k]`); separate names do not, so Design B cannot be looped, searched
   or passed to a function as one collection.
3. **Data and logic stay apart.** The 12-task program needs to reuse the same logic
   for reading, validating and totalling; with separate variables each of those
   would be repeated 300 times, so a rate change or a bug fix would need 300 edits:
   the same "changed in some places only" fault the co-operative already has.
4. **Real data arrives at run time.** The co-operative's clerk enters data and the
   analyser will supply it; *n* is not known when the program is written. Only
   Design A can read "as many entries as there are".
5. **It still works for the milk analyser and seasonal revisions.** Whatever
   source the entries come from, a list of tuples (or later a list of records) takes
   them unchanged; the rates live in one module.

**Conclusion:** Design A should be retained for the data layout; it is the one
design that stays correct, small and fast as 300 farmers become 150,000. (The
Design Challenge about the analyser and seasonal rates affects *where the rates
are stored*, not this choice.)