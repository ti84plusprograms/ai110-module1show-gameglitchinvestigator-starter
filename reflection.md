# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game, it asked me to make a guess between 1-100 and I had 7 attempts. One can also select their difficulty on the left side of the screen. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
After guessing 5 times and going between lower and higher, I wasn't getting the right answer. This was a bug. Also the show hint button wasn't making any UI changes, so I assumed that's also a bug. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Click "Show Hint" | A hint text appears or UI updates to show hint | No visible UI change when button clicked | No console errors |
| Make repeated guesses following higher/lower hints (e.g., guess 50, then 25, then 40) | Game eventually accepts correct number within remaining attempts and wins when guessed | After several logical higher/lower guesses the game still reports incorrect or doesn't end correctly | No console errors; logic seems wrong |
| Change difficulty from Easy to Hard | Number of attempts or difficulty setting updates accordingly | Difficulty selector changes visually but attempts remain the same / difficulty not applied | No console errors |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Codex as an AI coding teammate to inspect the repo, set up the virtual environment, install dependencies, identify bugs, write tests, and refactor the code. A correct AI suggestion was to move the game logic into `logic_utils.py` and test it separately, which I verified by running pytest after each set of changes. Another correct suggestion was to separate the outcome from the hint message, so `check_guess` returns `"Win"`, `"Too High"`, or `"Too Low"` while `get_hint_message` handles the display text. One thing I had to watch carefully was that AI could have filled in broad documentation too generically, so I verified the final notes against the actual files and pytest output.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed only after there was a focused pytest for the behavior and the full test suite passed. For example, `test_hint_messages_point_in_correct_direction` checks that a too-high guess tells the player to go lower and a too-low guess tells the player to go higher. I also ran tests for input parsing, score updates, difficulty ranges, game-state reset, and whether the app imports logic from `logic_utils.py` instead of redefining it. AI helped design the tests by turning each bug into a small expected behavior that could be checked automatically.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns the script from top to bottom whenever the user interacts with a widget, such as clicking a button or changing a selectbox. Normal Python variables can reset during those reruns, so values like the secret number, score, attempts, and history need to live in `st.session_state`. Session state works like a saved dictionary for the current user session. In this project, resetting all of the session-state values together made the game much more predictable.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is writing a test for each bug before moving on to the next fix. Next time I work with AI, I would ask it to explain the test strategy first so I can check whether the tests actually match the assignment. This project changed how I think about AI-generated code because the app looked plausible, but several small details made it unreliable. I learned that AI code still needs to be run, tested, and read carefully.
