# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the app it looked like a normal guessing game, but it was
unplayable in practice. The hints were backwards — guessing higher than the
secret told me to "Go HIGHER!" — so following the hints walked me away from the
answer. The secret also seemed to "change" because on even-numbered attempts the
code compared my integer guess against a string version of the secret, which
made the result inconsistent. On top of that the attempt counter started at 1
(off-by-one), "New Game" didn't reset the score/status/history, and running
`pytest` immediately failed because the `logic_utils.py` functions were
unimplemented stubs. The two clearest bugs at the start were the **backwards
hints** and the **shape-shifting (string-cast) secret**.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess higher than the secret (e.g. secret 50, guess 60) | Hint: "Go LOWER" | Hint said "📈 Go HIGHER!" (backwards) | None (logic bug) |
| Submit a 2nd guess (an even-numbered attempt) | Compare guess to the integer secret | Secret was cast to a string, so the comparison broke and gave a wrong/inconsistent result | None (silent `TypeError` caught and mishandled) |
| Open app, before guessing | "Attempts left" shows full limit (e.g. 8) | Showed limit − 1 because `attempts` started at 1 | None (off-by-one) |
| Click "New Game" after winning | Fresh game: new secret, score 0, attempts 0, status playing | Status/score/history stayed stale; secret re-rolled with hardcoded 1–100 range | None (incomplete state reset) |
| `pytest tests/` on the starter code | 3 tests pass | 3 tests failed | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

---

## 2. How did you use AI as a teammate?

**Tools used:** I used an AI coding assistant (Claude in agent mode) inside my
editor. I marked the "crime scenes" in the code with `# FIX` comments and asked
it to refactor the logic into `logic_utils.py` and fix the bugs one at a time.

**A suggestion that was correct:** The AI suggested moving `check_guess` into
`logic_utils.py` and fixing the hint direction so that a guess greater than the
secret returns `"Too High"`, with the player-facing text mapped to "Go LOWER".
I verified this two ways: (1) the existing pytest tests (`test_guess_too_high`,
`test_guess_too_low`) passed, and I added `test_hint_direction_is_not_reversed`
which also passed; and (2) I ran `streamlit run app.py`, guessed high, and saw
the hint correctly say "Go LOWER".

**A suggestion that was incorrect/misleading:** The original AI-generated
docstring for `check_guess` said it returns a tuple `(outcome, message)`. If I
had followed that contract, the unit tests (which assert `check_guess(50, 50) ==
"Win"`, a plain string) would have failed with something like
`assert ('Win', '🎉 Correct!') == 'Win'`. I caught this by reading the tests
first and running `pytest`, then changed `check_guess` to return only the
outcome string and moved the hint text into a `HINT_MESSAGES` dictionary in
`app.py`. Lesson: don't trust the AI's stated function contract — verify it
against the tests and callers.

---

## 3. Debugging and testing your fixes

**How I decided a bug was really fixed:** I used two checks for every fix — a
passing automated test *and* the same behavior confirmed in the live game. A bug
only counted as fixed when both agreed.

**A test I ran and what it showed:** For the "shape-shifting secret" bug I added
`test_compares_numerically_not_as_strings`, which asserts `check_guess(9, 10) ==
"Too Low"`. This is a sharp test because if the secret is ever compared as a
string, Python evaluates `"9" > "10"` as `True` and the function would wrongly
return `"Too High"`. Running `pytest` showed all 5 tests passing, which confirmed
the comparison stays numeric. I also ran the app and entered 9 against a secret
of 10 (visible in the Developer Debug Info panel) and got the correct "Go HIGHER"
hint.

**Did AI help with tests?** Yes. I asked the AI to generate a pytest case that
specifically targets each bug I fixed. It suggested the `check_guess(9, 10)`
case, and I checked the logic myself to confirm it would actually fail on the
old string-comparison code before trusting it as a regression test.

---

## 4. What did you learn about Streamlit and state?

I'd tell a friend that Streamlit re-runs the *entire* script from top to bottom
every time you interact with the page — every button click, text entry, or
widget change. That means any normal variable gets recreated from scratch on
each run, so if you stored the secret number in a plain variable it would be
re-randomized constantly. `st.session_state` is the fix: it's a dictionary that
*survives* across reruns, so values you put there (the secret, attempt count,
score, status, history) persist until you deliberately change them. The pattern
that made it click for me was "only initialize state if it isn't already there"
(`if "secret" not in st.session_state: ...`), and putting the full reset logic
in one `start_new_game()` helper so a button can rebuild state intentionally.

---

## 5. Looking ahead: your developer habits

The habit I most want to reuse is **verifying every fix two ways** — with an
automated pytest case *and* by actually playing the game — instead of assuming a
change worked just because the code looked right. I also want to keep the habit
of writing a sharp regression test that would *fail on the old bug* (like
`check_guess(9, 10)`, which catches string comparison), so the bug can't quietly
come back.

One thing I'd do differently is **read the existing tests and function callers
before accepting AI edits**, since the AI's stated function contract (a tuple
return) didn't match what the tests expected — catching that earlier would have
saved a step.

This project changed how I think about AI-generated code: it can look confident
and "production-ready" while being subtly and completely broken, so I now treat
AI output as a draft to be tested and reviewed, not as a finished answer.
