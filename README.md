# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** A Streamlit number-guessing game: the app
  picks a secret number within a range based on difficulty (Easy 1–20, Normal
  1–100, Hard 1–200), and the player guesses, getting "higher/lower" hints and a
  score, within a limited number of attempts.

- [x] **Detail which bugs you found.**
  1. **Backwards hints** — guessing too high told you to "Go HIGHER!" (and too low said "Go LOWER!").
  2. **Shape-shifting secret** — on even-numbered attempts the secret was cast to a string, so comparing the integer guess against it broke and produced wrong results.
  3. **Off-by-one attempts** — the attempt counter started at 1, so you lost an attempt before guessing and "Attempts left" was wrong.
  4. **Broken "New Game"** — it only reset the attempt counter and re-rolled the secret with a hardcoded 1–100 range; it never reset the score, game status, or history, so a finished game couldn't truly restart.
  5. **Hardcoded prompt** — the instructions always said "between 1 and 100" even on Easy/Hard.
  6. **Nonsense scoring** — points were added/subtracted inconsistently (alternating ±5) on wrong guesses.
  7. **Hard was easier than Normal** — Hard used range 1–50 vs Normal's 1–100.

- [x] **Explain what fixes you applied.**
  - Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` into `logic_utils.py`.
  - Fixed the hint directions (Too High → "Go LOWER", Too Low → "Go HIGHER").
  - Removed the even-attempt `str(secret)` conversion so the secret is always compared as an integer.
  - Initialized `attempts` to 0 and used the difficulty range everywhere (prompt + secret generation).
  - Added a single `start_new_game()` helper that resets secret, attempts, score, status, and history.
  - Simplified scoring: a win awards `100 - 10 × (attempts − 1)` points (minimum 10); non-winning guesses don't change the score.
  - Made Hard genuinely harder (range 1–200).
  - Changed `check_guess` to return a plain outcome string (`"Win"`/`"Too High"`/`"Too Low"`) so it satisfies the unit tests; the user-facing hint text now lives in a `HINT_MESSAGES` map in `app.py`.

## 📸 Demo Walkthrough

A text-based record of one full game so a reader can follow the end-to-end
behavior without running it. (Difficulty: **Normal**, range 1–100, 8 attempts.
Secret for this sample run = **63**, visible via "Developer Debug Info".)

1. App launches; sidebar shows "Range: 1 to 100" and "Attempts allowed: 8". The prompt reads "Attempts left: 8" and the score starts at 0.
2. User enters a guess of **50** → outcome **Too Low**, hint "📈 Go HIGHER!". Attempts left: 7. Score still 0.
3. User enters a guess of **75** → outcome **Too High**, hint "📉 Go LOWER!". Attempts left: 6. Score still 0.
4. User enters a guess of **60** → outcome **Too Low**, hint "📈 Go HIGHER!". Attempts left: 5. Score still 0.
5. User enters a guess of **63** → outcome **Win** 🎉. Balloons appear and the score updates to **80** (`100 − 10 × (4 − 1)`, since the win came on the 4th attempt).
6. The board shows "You won! The secret was 63. Final score: 80" and locks further guessing.
7. User clicks "New Game 🔁" → state fully resets (new secret, score 0, attempts 0, cleared history) and play can begin again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0
collected 22 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  4%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [  9%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 13%]
tests/test_game_logic.py::test_hint_direction_is_not_reversed PASSED     [ 18%]
tests/test_game_logic.py::test_compares_numerically_not_as_strings PASSED [ 22%]
tests/test_game_logic.py::test_parse_negative_number PASSED              [ 27%]
tests/test_game_logic.py::test_check_negative_guess_is_too_low PASSED    [ 31%]
tests/test_game_logic.py::test_parse_decimal_truncates_to_int PASSED     [ 36%]
tests/test_game_logic.py::test_parse_negative_decimal PASSED             [ 40%]
tests/test_game_logic.py::test_parse_extremely_large_number PASSED       [ 45%]
tests/test_game_logic.py::test_check_extremely_large_guess_is_too_high PASSED [ 50%]
tests/test_game_logic.py::test_invalid_inputs_return_clean_error[-Enter a guess.] PASSED [ 54%]
tests/test_game_logic.py::test_invalid_inputs_return_clean_error[   -Enter a guess.] PASSED [ 59%]
tests/test_game_logic.py::test_invalid_inputs_return_clean_error[None-Enter a guess.] PASSED [ 63%]
tests/test_game_logic.py::test_invalid_inputs_return_clean_error[abc-That is not a number.] PASSED [ 68%]
tests/test_game_logic.py::test_invalid_inputs_return_clean_error[10abc-That is not a number.] PASSED [ 72%]
tests/test_game_logic.py::test_invalid_inputs_return_clean_error[1,000-That is not a number.] PASSED [ 77%]
tests/test_game_logic.py::test_invalid_inputs_return_clean_error[NaN-That is not a number.] PASSED [ 81%]
tests/test_game_logic.py::test_high_score_defaults_to_zero_when_missing PASSED [ 86%]
tests/test_game_logic.py::test_save_and_load_high_score_round_trip PASSED [ 90%]
tests/test_game_logic.py::test_update_high_score_keeps_the_best PASSED   [ 95%]
tests/test_game_logic.py::test_load_high_score_survives_corrupt_file PASSED [100%]

============================== 22 passed in 0.04s ==============================
```

## 🚀 Stretch Features

### Challenge 1 — Advanced Edge-Case Testing
Added a suite of edge-case tests in [`tests/test_game_logic.py`](tests/test_game_logic.py)
covering **negative numbers**, **decimals** (truncated to int), and **extremely
large values** (100-digit numbers / `10**50`), plus a parametrized set of
invalid inputs (blank, whitespace, `None`, letters, `"10abc"`, `"1,000"`,
`"NaN"`) that must return a clean error instead of crashing. The full passing
output is in the **Test Results** section above (22 tests).

### Challenge 2 — Feature Expansion: High Score tracker
Added persistent high-score tracking. New functions in
[`logic_utils.py`](logic_utils.py) — `load_high_score`, `save_high_score`, and
`update_high_score` — read/write the best score to `high_score.json` (git-ignored).
On a win, [`app.py`](app.py) calls `update_high_score(...)`, and the **🏅 High
score** metric in the stats row shows the all-time best across sessions. The
loader is crash-safe: a missing or corrupt file returns `0` rather than raising.

### Challenge 3 — Professional Documentation & Linting
Every function in [`logic_utils.py`](logic_utils.py) now has a Google-style
docstring (Args/Returns). Ran `flake8` for PEP 8 compliance and fixed all
findings (unused import, blank-line spacing). See `ai_interactions.md` for the
before/after lint output.

### Challenge 4 — Enhanced Game UI
The UI in [`app.py`](app.py) was redesigned (logic untouched):
- **Gradient header card** via injected CSS (`.gg-header`).
- **Live stat metrics** — Score, High score, Attempts used, Attempts left —
  rendered after the guess is processed so they're always current.
- **Progress bar** showing attempts consumed (`st.progress`).
- **Color-coded feedback banner** driven by the `OUTCOME_STYLE` map
  (green = win, red = too high/loss, blue = too low, gray = invalid).
- **Warmth meter** — 🔥/🌡️/😐/❄️ proximity hint based on the last guess's
  distance to the secret (relative to the range, so it never reveals the answer).
- **Guess-history chips** — each past guess shown as a colored pill reflecting
  its outcome (history now stores `{"guess", "outcome"}` entries).
- **Cleaner controls** — full-width buttons disabled when the game is over, and
  the debug panel moved behind a sidebar toggle (off by default).
