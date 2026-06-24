from logic_utils import check_guess

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
