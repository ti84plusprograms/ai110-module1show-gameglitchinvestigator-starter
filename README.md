# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Create and activate a virtual environment:
   `python3 -m venv .venv`
   `source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

The game is a Streamlit number guessing game where the player chooses a difficulty, guesses the secret number, and uses higher/lower hints to find the answer before running out of attempts.

Bugs found:

- The shared logic module was unfinished, so pytest failed with `NotImplementedError`.
- The app kept duplicated game logic inside `app.py` instead of using `logic_utils.py`.
- The hint messages were backwards.
- The app sometimes converted the secret number to a string before comparing it to the guess.
- Attempts started at `1`, which made the attempts-left display wrong.
- New Game did not reset score, status, history, or difficulty-aware secret generation.
- Hard difficulty used a smaller range than Normal.
- The UI always said `1` to `100` even when another difficulty was selected.

Fixes applied:

- Implemented and tested `check_guess`, `parse_guess`, `get_range_for_difficulty`, `get_attempt_limit`, `get_hint_message`, `update_score`, and `reset_game_state`.
- Refactored `app.py` to import logic from `logic_utils.py`.
- Fixed hint direction text.
- Kept the secret number numeric during comparisons.
- Reset attempts to `0` for new games and difficulty changes.
- Reset all round state when starting a new game.
- Generated new secrets from the selected difficulty range.
- Updated the UI to display the active range.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the app with `python -m streamlit run app.py`.
2. Select a difficulty from the sidebar and confirm the displayed range and attempt limit.
3. Enter a whole-number guess and click Submit Guess.
4. Use the hint message to decide whether the next guess should be lower or higher.
5. Continue guessing until the app shows the winning message or the attempt limit is reached.
6. Click New Game to reset the secret number, attempts, score, status, and history.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
python -m pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.10.6, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/ary/Documents/GitHub/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 10 items

tests/test_game_logic.py ..........                                      [100%]

============================== 10 passed in 0.10s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
