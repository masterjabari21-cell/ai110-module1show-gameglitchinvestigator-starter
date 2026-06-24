"""Pure game logic for the Number Guessing Game.

This module holds all the rules of the game with no Streamlit/UI code, so the
functions can be unit-tested in isolation. The Streamlit front end in
``app.py`` imports and calls these functions.
"""

import json

#: Default file used to persist the all-time best score across sessions.
HIGH_SCORE_FILE = "high_score.json"


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.

    Returns:
        A ``(low, high)`` tuple of inclusive bounds. Unknown difficulties
        fall back to the Normal range ``(1, 100)``.
    """
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into an integer guess.

    Decimal strings are truncated toward zero (``"3.9"`` -> ``3``); blank or
    non-numeric input is rejected with a friendly message rather than raising.

    Args:
        raw: The raw string entered by the player (may be ``None``).

    Returns:
        A ``(ok, guess, error)`` tuple where ``ok`` is ``True`` on success with
        ``guess`` set and ``error`` ``None``; on failure ``ok`` is ``False``,
        ``guess`` is ``None`` and ``error`` is a human-readable message.
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


def check_guess(guess: int, secret: int) -> str:
    """Compare a guess to the secret number and return the outcome.

    Args:
        guess: The player's numeric guess.
        secret: The secret number to compare against.

    Returns:
        One of ``"Win"``, ``"Too High"``, or ``"Too Low"``.
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


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Compute the new score after a guess.

    A win awards more points the fewer attempts it took, with a floor of 10.
    Non-winning outcomes leave the score unchanged.

    Args:
        current_score: The score before this guess.
        outcome: The outcome from :func:`check_guess`.
        attempt_number: 1-based count of the attempt that produced ``outcome``.

    Returns:
        The updated score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)
    return current_score


def load_high_score(path: str = HIGH_SCORE_FILE) -> int:
    """Read the persisted all-time high score.

    Args:
        path: Path to the JSON file storing the high score.

    Returns:
        The stored high score, or ``0`` if the file is missing or unreadable.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return int(json.load(f).get("high_score", 0))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0


def save_high_score(score: int, path: str = HIGH_SCORE_FILE) -> None:
    """Write ``score`` to the high-score file, ignoring I/O errors.

    Args:
        score: The score to persist.
        path: Path to the JSON file storing the high score.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"high_score": int(score)}, f)
    except OSError:
        # Persisting the high score is best-effort; never crash the game.
        pass


def update_high_score(score: int, path: str = HIGH_SCORE_FILE) -> int:
    """Persist ``score`` only if it beats the stored high score.

    Args:
        score: The candidate score (typically the final score of a won game).
        path: Path to the JSON file storing the high score.

    Returns:
        The resulting high score after the comparison.
    """
    best = load_high_score(path)
    if score > best:
        save_high_score(score, path)
        return score
    return best
