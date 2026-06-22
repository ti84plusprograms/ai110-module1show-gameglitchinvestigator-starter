# Project Report: Game Glitch Investigator

## Repository Summary

This repo is a starter lab for debugging an AI-generated Streamlit number guessing game. The assignment asks the developer to play the broken game, identify state and logic bugs, refactor game logic into `logic_utils.py`, run tests, and document the debugging process in `reflection.md`.

## Environment Setup

- Created a local virtual environment at `.venv/`.
- Installed dependencies from `requirements.txt` into that environment.
- Key installed packages:
  - `streamlit 1.58.0`
  - `altair 4.2.2`
  - `pytest 9.0.3`
- `.venv/` is already ignored by `.gitignore`.

Useful commands:

```bash
source .venv/bin/activate
python -m streamlit run app.py
python -m pytest tests/
```

## Initial Test Baseline

Command run:

```bash
.venv/bin/python -m pytest tests/
```

Result:

```text
3 failed in 0.17s
```

All failures come from `logic_utils.check_guess`, which currently raises `NotImplementedError`.

## Important Files

- `README.md`: Assignment instructions, setup steps, mission checklist, and documentation requirements.
- `app.py`: Current Streamlit app. It contains game logic directly in the app file, including several intentional bugs.
- `logic_utils.py`: Placeholder module where logic should be refactored.
- `tests/test_game_logic.py`: Tests for `check_guess`.
- `reflection.md`: Student reflection template.
- `ai_interactions.md`: Optional stretch-feature log for AI usage.

## Bugs And Issues Found

1. `logic_utils.py` is unfinished.
   - Every function raises `NotImplementedError`.
   - Existing tests import `check_guess` from this file, so tests cannot pass yet.

2. `app.py` still owns the game logic.
   - The README asks for logic to be moved into `logic_utils.py`.
   - Keeping duplicate logic in `app.py` and `logic_utils.py` would make future fixes harder to verify.

3. Hint messages are backwards in `app.py`.
   - When `guess > secret`, the game returns `"Too High"` but displays `"Go HIGHER!"`.
   - When `guess < secret`, the game returns `"Too Low"` but displays `"Go LOWER!"`.

4. Secret type changes during gameplay.
   - On even-numbered attempts, `app.py` converts the secret number to a string before calling `check_guess`.
   - This can cause incorrect comparisons or strange behavior.

5. Attempt counting starts at `1`.
   - A new session initializes `attempts` to `1`, so the display begins with one attempt already consumed.
   - The submit handler increments attempts before checking the guess.

6. New game reset is incomplete.
   - The new game button resets `attempts` and `secret`, but it does not reset `score`, `status`, or `history`.
   - It also always uses `random.randint(1, 100)` instead of the selected difficulty range.

7. Difficulty range behavior is inconsistent.
   - `get_range_for_difficulty("Hard")` returns `1, 50`, which makes Hard use a smaller range than Normal.
   - The UI still says "Guess a number between 1 and 100" regardless of the selected difficulty.

8. Existing tests and function behavior do not currently match.
   - `app.py` has `check_guess` returning `(outcome, message)`.
   - `tests/test_game_logic.py` expects `check_guess` to return only the outcome string.
   - The implementation should be aligned with the tests, or the tests should be updated intentionally.

## Recommended Next Steps

1. Implement `logic_utils.check_guess` so the current tests pass.
2. Decide whether `check_guess` should return only an outcome string or an `(outcome, message)` tuple, then align both app code and tests.
3. Move `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` and import them from `logic_utils.py`.
4. Fix the backwards hint messages.
5. Remove the string conversion of `secret` during gameplay.
6. Initialize attempts at `0` and make the attempts-left display consistent.
7. Reset `score`, `status`, and `history` when starting a new game.
8. Generate the new secret using the selected difficulty range.
9. Update the UI text so it shows the active low/high range.
10. Add or update tests for:
    - winning guesses
    - too-high and too-low guesses
    - input parsing
    - difficulty ranges
    - score updates
11. Run `python -m pytest tests/` until all tests pass.
12. Manually run the Streamlit app and document the final behavior in `reflection.md`.

## Completed Fix Log

### Fix Gate 1: Utility Logic Contract

Status: fixed and tested.

What changed:

- Implemented `logic_utils.check_guess` so it returns the outcome string expected by the original tests: `"Win"`, `"Too High"`, or `"Too Low"`.
- Added `logic_utils.get_hint_message` so display text is separate from comparison logic and the hint direction can be tested directly.
- Implemented `logic_utils.parse_guess`, `get_range_for_difficulty`, `get_attempt_limit`, and `update_score`.
- Chose the contract where `check_guess` returns only the outcome string; the app can ask `get_hint_message` for display copy.
- Updated Hard difficulty to use a larger range, `1` to `200`, so it is harder than Normal.

Tests written:

- `test_winning_guess`
- `test_guess_too_high`
- `test_guess_too_low`
- `test_hint_messages_point_in_correct_direction`
- `test_parse_guess_accepts_whole_number_with_spaces`
- `test_parse_guess_rejects_empty_or_non_whole_number`
- `test_difficulty_ranges_get_harder`
- `test_attempt_limits_by_difficulty`
- `test_update_score_rewards_fast_wins_and_penalizes_misses`

Pytest result before continuing:

```text
9 passed in 0.06s
```

### Fix Gate 2: Resettable Game State

Status: fixed and tested.

What changed:

- Added `logic_utils.reset_game_state` to reset all round-specific values in one place.
- The helper sets `attempts` to `0`, clears `history`, resets `score`, restores `status` to `"playing"`, stores the selected `difficulty`, and accepts a caller-generated `secret`.
- This prepares the app to start new games cleanly and to generate secrets using the current difficulty range.

Tests written:

- `test_reset_game_state_clears_round_data`

Pytest result before continuing:

```text
10 passed in 0.22s
```

### Fix Gate 3: Streamlit App Refactor And State Fixes

Status: fixed and tested.

What changed:

- Refactored `app.py` to import game logic from `logic_utils.py` instead of redefining it locally.
- Updated the app to call `get_hint_message`, so hint text now points in the correct direction.
- Removed the even-attempt conversion of `secret` to a string; guesses are compared against the numeric secret consistently.
- Changed initial game setup to use `reset_game_state`, so attempts begin at `0`.
- Updated new-game behavior to reset `attempts`, `score`, `status`, `history`, `difficulty`, and `secret`.
- Changed new-game secret generation to use the selected difficulty range.
- Updated the on-screen prompt to show the active range with `{low}` and `{high}` instead of always saying `1` to `100`.
- Added a difficulty-change reset so switching difficulty starts a fresh round with a secret in the correct range.

Tests written:

- No separate app test file was kept.
- The refactor relies on the tested `logic_utils.py` contract in `tests/test_game_logic.py`.

Pytest result before continuing:

```text
10 passed in 0.10s
```

### Fix Gate 4: Project Documentation

Status: fixed and ready for final verification.

What changed:

- Updated `README.md` with virtual environment setup, fixed-game purpose, bugs found, fixes applied, a demo walkthrough, and pytest output.
- Updated `reflection.md` sections 2 through 5 with the AI collaboration process, debugging and testing approach, Streamlit session-state explanation, and future developer habits.
- Preserved the existing section 1 notes and bug reproduction log already present in `reflection.md`.

Tests written:

- No new pytest was needed for Markdown-only documentation changes.
- The full existing pytest suite was run again before final verification.

Pytest result before continuing:

```text
10 passed in 0.08s
```

### Final Verification

Status: complete.

Checks run:

- `.venv/bin/python -m pytest tests/`
- `.venv/bin/python -m py_compile app.py logic_utils.py tests/test_game_logic.py`
- `.venv/bin/python -m streamlit run app.py --server.headless true --server.port 8502`

Results:

- Pytest passed with 10 tests in 0.10 seconds.
- Python compilation passed.
- Streamlit started successfully on `http://localhost:8502`.
- The temporary Streamlit verification server was stopped after startup was confirmed.

## Documentation Still To Complete

- Optionally add a screenshot of the fixed, winning game to `README.md`.
- Use `ai_interactions.md` only if stretch features involving AI workflows, test generation, linting, or model comparison are attempted.
