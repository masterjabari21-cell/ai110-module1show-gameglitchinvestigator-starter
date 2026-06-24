import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    load_high_score,
    update_high_score,
)

# FIX (Bug 1 - backwards hints): refactored the hint text out of check_guess
# and corrected the direction with AI agent mode. A "Too High" guess must tell
# the player to go LOWER (the starter code had these reversed).
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

# Visual style (color + emoji) for each outcome, reused by the feedback banner
# and the guess-history chips.
OUTCOME_STYLE = {
    "Win": ("#1b7f4b", "#d6f5e3", "🎉"),
    "Too High": ("#b3261e", "#fdecea", "📉"),
    "Too Low": ("#1f5fb3", "#e8f0fe", "📈"),
    "Invalid": ("#6b6b6b", "#eeeeee", "⚠️"),
}

st.set_page_config(
    page_title="Glitchy Guesser",
    page_icon="🎮",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
      .gg-header {
        background: linear-gradient(135deg, #6d5dfc 0%, #8f6ed5 100%);
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        color: #ffffff;
        box-shadow: 0 8px 24px rgba(109, 93, 252, 0.25);
        margin-bottom: 1.2rem;
      }
      .gg-header h1 { margin: 0; font-size: 1.9rem; }
      .gg-header p { margin: 0.3rem 0 0; opacity: 0.9; font-size: 0.95rem; }
      .gg-banner {
        padding: 0.9rem 1.1rem;
        border-radius: 12px;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0.4rem 0 0.8rem;
      }
      .gg-chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.3rem; }
      .gg-chip {
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
      }
      div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.45rem 0.2rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="gg-header">
      <h1>🎮 Game Glitch Investigator</h1>
      <p>The once-glitchy guessing game — now debugged and playable.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar settings
# ---------------------------------------------------------------------------
st.sidebar.header("⚙️ Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.metric("Range", f"{low} – {high}")
st.sidebar.metric("Attempts allowed", attempt_limit)
show_debug = st.sidebar.toggle("🔧 Developer debug info", value=False)


def start_new_game():
    """Reset all game state for a fresh round at the current difficulty."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_outcome = None
    st.session_state.last_message = ""
    st.session_state.last_guess = None


# Initialize state once. Because these live in st.session_state, they persist
# across Streamlit reruns (every button click triggers a full rerun).
if "secret" not in st.session_state:
    start_new_game()

playing = st.session_state.status == "playing"

# ---------------------------------------------------------------------------
# Guess input + controls
# ---------------------------------------------------------------------------
st.subheader("🎯 Make a guess")
st.caption(f"Pick a whole number between **{low}** and **{high}**.")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
    placeholder=f"{low}–{high}",
    disabled=not playing,
)

col1, col2, col3 = st.columns([1.2, 1.2, 1])
with col1:
    submit = st.button("Submit Guess 🚀", use_container_width=True, disabled=not playing)
with col2:
    new_game = st.button("New Game 🔁", use_container_width=True)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# ---------------------------------------------------------------------------
# Handle controls (mutate state before rendering the stats below)
# ---------------------------------------------------------------------------
if new_game:
    start_new_game()
    st.rerun()

if submit and playing:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append({"guess": raw_guess, "outcome": "Invalid"})
        st.session_state.last_outcome = "Invalid"
        st.session_state.last_message = err
        st.session_state.last_guess = raw_guess
    else:
        st.session_state.attempts += 1

        # FIX (Bug 2 - shape-shifting secret): the starter code cast the secret
        # to str() on even-numbered attempts before calling check_guess, so the
        # comparison silently broke. We now always pass the integer secret.
        outcome = check_guess(guess_int, st.session_state.secret)

        st.session_state.history.append({"guess": guess_int, "outcome": outcome})
        st.session_state.last_outcome = outcome
        st.session_state.last_message = HINT_MESSAGES[outcome]
        st.session_state.last_guess = guess_int

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            # High Score feature: persist the best score across sessions.
            update_high_score(st.session_state.score)
            st.balloons()
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"

    playing = st.session_state.status == "playing"

# ---------------------------------------------------------------------------
# Live stats
# ---------------------------------------------------------------------------
attempts_used = st.session_state.attempts
attempts_left = max(attempt_limit - attempts_used, 0)
high_score = max(load_high_score(), st.session_state.score)

m1, m2, m3, m4 = st.columns(4)
m1.metric("⭐ Score", st.session_state.score)
m2.metric("🏅 High score", high_score)
m3.metric("🎲 Attempts used", f"{attempts_used} / {attempt_limit}")
m4.metric("⏳ Attempts left", attempts_left)

st.progress(min(attempts_used / attempt_limit, 1.0))

# ---------------------------------------------------------------------------
# Feedback banner
# ---------------------------------------------------------------------------
secret = st.session_state.secret

if st.session_state.status == "won":
    fg, bg, _ = OUTCOME_STYLE["Win"]
    st.markdown(
        f'<div class="gg-banner" style="color:{fg};background:{bg};">'
        f"🏆 You won! The secret was {secret}. Final score: "
        f"{st.session_state.score}</div>",
        unsafe_allow_html=True,
    )
elif st.session_state.status == "lost":
    fg, bg, _ = OUTCOME_STYLE["Too High"]
    st.markdown(
        f'<div class="gg-banner" style="color:{fg};background:{bg};">'
        f"💥 Out of attempts! The secret was {secret}. "
        f"Score: {st.session_state.score}</div>",
        unsafe_allow_html=True,
    )
elif st.session_state.last_outcome == "Invalid":
    fg, bg, emoji = OUTCOME_STYLE["Invalid"]
    st.markdown(
        f'<div class="gg-banner" style="color:{fg};background:{bg};">'
        f"{emoji} {st.session_state.last_message}</div>",
        unsafe_allow_html=True,
    )
elif st.session_state.last_outcome and show_hint:
    fg, bg, _ = OUTCOME_STYLE[st.session_state.last_outcome]
    st.markdown(
        f'<div class="gg-banner" style="color:{fg};background:{bg};">'
        f"{st.session_state.last_message}</div>",
        unsafe_allow_html=True,
    )

# Warmth meter: how close the last valid guess was, without revealing the secret.
if playing and isinstance(st.session_state.last_guess, int):
    span = max(high - low, 1)
    distance = abs(st.session_state.last_guess - secret)
    closeness = distance / span
    if closeness <= 0.05:
        warmth = "🔥 Boiling hot!"
    elif closeness <= 0.15:
        warmth = "🌡️ Hot"
    elif closeness <= 0.35:
        warmth = "😐 Warm"
    else:
        warmth = "❄️ Cold"
    st.caption(f"Proximity: {warmth}")

# ---------------------------------------------------------------------------
# Guess history
# ---------------------------------------------------------------------------
if st.session_state.history:
    st.markdown("##### 📜 Your guesses")
    chips = []
    for entry in st.session_state.history:
        fg, bg, emoji = OUTCOME_STYLE[entry["outcome"]]
        chips.append(
            f'<span class="gg-chip" style="color:{fg};background:{bg};">'
            f'{emoji} {entry["guess"]}</span>'
        )
    st.markdown(
        f'<div class="gg-chips">{"".join(chips)}</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Developer debug info (hidden behind a sidebar toggle)
# ---------------------------------------------------------------------------
if show_debug:
    with st.expander("Developer Debug Info", expanded=True):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

st.divider()
st.caption("Refactored, debugged, and redesigned. No more lying hints. 💚")
