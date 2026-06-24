# AI Interactions Log

> **Stretch features.** Documents the AI-assisted work for the stretch
> challenges I attempted (Challenges 1, 2, 3, 5).

---

## Agent Workflow (SF8) — Challenge 2: High Score feature

> Document your experience using an AI agent to make multi-step changes autonomously.

**What task did you give the agent?**

"Implement a persistent High Score tracker: add functions to `logic_utils.py`
that save/load the best score to a file, wire it into `app.py` so the best score
updates on a win and shows in the stats row, and add tests for it."

**What did the agent do?**

- Added `load_high_score`, `save_high_score`, and `update_high_score` to
  [`logic_utils.py`](logic_utils.py), persisting to `high_score.json` via the
  `json` module, with all errors (missing/corrupt file) caught so the game never
  crashes.
- Modified [`app.py`](app.py): imported the new functions, called
  `update_high_score(...)` when the player wins, and added a **🏅 High score**
  metric to the stats row.
- Added `high_score.json` to [`.gitignore`](.gitignore).
- Added 4 tests in [`tests/test_game_logic.py`](tests/test_game_logic.py) using
  pytest's `tmp_path` fixture so no real file is touched.

**Files modified:** `logic_utils.py`, `app.py`, `.gitignore`, `tests/test_game_logic.py`.

**What did you have to verify or fix manually?**

- Confirmed the high-score metric shows the live best by using
  `max(load_high_score(), current_score)` so it updates within the same session,
  not only after a reload.
- Verified the corrupt-file case returns `0` instead of raising (added
  `test_load_high_score_survives_corrupt_file`).
- Ran the app headless to confirm it boots cleanly with the new code.

---

## Test Generation (SF7) — Challenge 1: Advanced Edge-Case Testing

> How I used AI to generate edge-case tests.

**Prompt used:** "Identify three edge-case inputs that might still break this
guessing game and generate a pytest suite that verifies the game handles them
gracefully. Cover negative numbers, decimals, and extremely large values, and
add cases for invalid/garbage input."

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning (why this case) |
|-----------|-------------|-------------------|--------------|--------------------------------|
| Negative number | (above) | `parse_guess("-5")` → `(True, -5, None)`; `check_guess(-5, 50)` == "Too Low" | ✅ | Minus signs are valid ints and must compare correctly, not be rejected. |
| Decimal | (above) | `parse_guess("3.9")` → value `3` (truncated) | ✅ | Users may type decimals; the game truncates to an int rather than crashing. |
| Extremely large value | (above) | `parse_guess("9"*100)`; `check_guess(10**50, 50)` == "Too High" | ✅ | Python big ints shouldn't overflow — confirms no numeric limit breaks the compare. |
| Blank / whitespace / None | (above) | `parse_guess("")`, `"   "`, `None` → "Enter a guess." | ✅ | Empty submits must give a friendly prompt, not an exception. |
| Non-numeric / mixed | (above) | `"abc"`, `"10abc"`, `"1,000"`, `"NaN"` → "That is not a number." | ✅ | Garbage input must fail gracefully with a clean message. |

All 22 tests pass (see README **Test Results**).

---

## Linting & Style (SF9) — Challenge 3

> Use of AI for linting / code style.

**Prompt used:**

```
Add professional Google-style docstrings to every function in logic_utils.py,
then run flake8 for PEP 8 compliance and fix any findings.
```

**Linting output BEFORE (flake8, --max-line-length=100):**

```
logic_utils.py:9:1: F401 'os' imported but unused
tests/test_game_logic.py:11:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:16:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:21:1: E302 expected 2 blank lines, found 1
```

**Linting output AFTER:**

```
$ flake8 logic_utils.py app.py tests/test_game_logic.py --max-line-length=100
(no output — exit code 0)
```

**Changes applied:**

- Removed the unused `import os` from `logic_utils.py` (F401).
- Added the missing blank lines between the starter test functions so each
  top-level function has two blank lines before it (E302).
- Added Google-style docstrings (Args/Returns) to all six functions in
  `logic_utils.py`. I accepted all of these suggestions because they were
  mechanical PEP 8 fixes with no behavior change, and re-ran the test suite
  (22 passing) to confirm nothing broke.

---

## Model Comparison (SF11) — Challenge 5

> Compare two AI models fixing the same Phase 1 bug.

**Bug chosen:** the backwards-hint bug in `check_guess` (a guess greater than the
secret should report "Too High").

**⚠️ Honesty note:** The "Model A" column below is the *actual* fix produced by
Claude in this session. I have **not** run a second model, so the "Model B"
column is a placeholder — to complete this challenge, paste the same bug into
another assistant (e.g., Gemini, ChatGPT, or Copilot), record its real response
here, and then fill in the comparison rows from what you observe. Do not submit
the placeholder as if it were a real run.

**Task given to both models:** "This `check_guess` function reports the wrong
direction — fix it so a guess above the secret returns 'Too High'. Explain why."

| | Model A (Claude — actual) | Model B (run yourself) |
|-|---------------------------|------------------------|
| **Model name** | claude-sonnet-4-6 | _<paste model name>_ |
| **Response summary** | Separated the outcome from the message: `check_guess` returns just `"Win"/"Too High"/"Too Low"`, and the hint text moved to a `HINT_MESSAGES` map in `app.py`. Noted that the tests expect a plain string, not a tuple. | _<paste summary>_ |
| **More Pythonic?** | Simple guard clauses, no nested branches; matches the unit-test contract. | _<your judgment>_ |
| **Clearer explanation?** | Explained both the direction fix *and* the related string-comparison bug, and pointed to the regression test. | _<your judgment>_ |

**Which did you prefer and why?**

_<Fill in after you run the second model and compare the two responses.>_
