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
collected 5 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 20%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 40%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 60%]
tests/test_game_logic.py::test_hint_direction_is_not_reversed PASSED     [ 80%]
tests/test_game_logic.py::test_compares_numerically_not_as_strings PASSED [100%]

============================== 5 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
