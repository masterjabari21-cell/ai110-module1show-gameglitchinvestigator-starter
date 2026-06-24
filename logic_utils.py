def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    Returns one of: "Win", "Too High", "Too Low"
    """
    # FIX (Bug 1 - backwards hints): the original returned the wrong outcome/
    # message direction. Worked with the AI to confirm guess > secret == "Too
    # High". The matching player-facing hint ("Go LOWER") lives in app.py.
    # FIX (Bug 2 - shape-shifting secret): compare as numbers, never as strings.
    # The old app.py cast the secret to str() on even attempts, which made
    # comparisons like 9 vs 10 wrong ("9" > "10"). Keeping both operands numeric
    # here is guarded by a regression test in tests/test_game_logic.py.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    A win awards more points the fewer attempts it took (minimum 10).
    Non-winning outcomes leave the score unchanged.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)
    return current_score
