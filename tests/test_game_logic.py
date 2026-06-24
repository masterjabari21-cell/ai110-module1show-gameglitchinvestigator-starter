import pytest

from logic_utils import (
    check_guess,
    parse_guess,
    load_high_score,
    save_high_score,
    update_high_score,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Regression test for Bug 1: backwards hints ---
def test_hint_direction_is_not_reversed():
    # A larger guess than the secret must be "Too High" (the starter code
    # reported the opposite direction).
    assert check_guess(75, 30) == "Too High"
    assert check_guess(30, 75) == "Too Low"


# --- Regression test for Bug 2: shape-shifting (string-cast) secret ---
def test_compares_numerically_not_as_strings():
    # 9 < 10 numerically, so this is "Too Low".
    # If the secret were compared as a string ("9" > "10"), this would wrongly
    # return "Too High" -- exactly the bug caused by str(secret) in app.py.
    assert check_guess(9, 10) == "Too Low"


# ===========================================================================
# Challenge 1: Advanced Edge-Case Testing
#
# Three categories of "weird" input that could still break the game:
#   1. Negative numbers   -> valid integers; must compare correctly.
#   2. Decimal strings    -> truncated to int by parse_guess, not rejected.
#   3. Extremely large    -> Python big ints must not overflow or crash.
# Plus a few "garbage input" cases to confirm the game fails gracefully
# (returns a clean error message instead of raising).
# ===========================================================================

# --- Edge case 1: negative numbers ---
def test_parse_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_check_negative_guess_is_too_low():
    # -5 is well below a secret of 50.
    assert check_guess(-5, 50) == "Too Low"


# --- Edge case 2: decimals ---
def test_parse_decimal_truncates_to_int():
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3          # truncated, not rounded
    assert err is None


def test_parse_negative_decimal():
    ok, value, err = parse_guess("-2.5")
    assert ok is True
    assert value == -2
    assert err is None


# --- Edge case 3: extremely large values ---
def test_parse_extremely_large_number():
    big = "9" * 100  # a 100-digit number
    ok, value, err = parse_guess(big)
    assert ok is True
    assert value == int(big)
    assert err is None


def test_check_extremely_large_guess_is_too_high():
    assert check_guess(10 ** 50, 50) == "Too High"


# --- Graceful handling of invalid input ---
@pytest.mark.parametrize(
    "raw, expected_error",
    [
        ("", "Enter a guess."),
        ("   ", "Enter a guess."),
        (None, "Enter a guess."),
        ("abc", "That is not a number."),
        ("10abc", "That is not a number."),
        ("1,000", "That is not a number."),
        ("NaN", "That is not a number."),
    ],
)
def test_invalid_inputs_return_clean_error(raw, expected_error):
    ok, value, err = parse_guess(raw)
    assert ok is False
    assert value is None
    assert err == expected_error


# ===========================================================================
# Challenge 2: High Score tracker (file persistence)
# ===========================================================================
def test_high_score_defaults_to_zero_when_missing(tmp_path):
    path = str(tmp_path / "missing.json")
    assert load_high_score(path) == 0


def test_save_and_load_high_score_round_trip(tmp_path):
    path = str(tmp_path / "hs.json")
    save_high_score(80, path)
    assert load_high_score(path) == 80


def test_update_high_score_keeps_the_best(tmp_path):
    path = str(tmp_path / "hs.json")
    assert update_high_score(50, path) == 50   # first score becomes the best
    assert update_high_score(30, path) == 50   # lower score does not replace
    assert update_high_score(90, path) == 90   # higher score wins
    assert load_high_score(path) == 90


def test_load_high_score_survives_corrupt_file(tmp_path):
    path = tmp_path / "hs.json"
    path.write_text("not valid json {", encoding="utf-8")
    assert load_high_score(str(path)) == 0
