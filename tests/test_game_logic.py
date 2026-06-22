from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    reset_game_state,
    update_score,
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


def test_hint_messages_point_in_correct_direction():
    assert "lower" in get_hint_message("Too High").lower()
    assert "higher" in get_hint_message("Too Low").lower()
    assert "correct" in get_hint_message("Win").lower()


def test_parse_guess_accepts_whole_number_with_spaces():
    assert parse_guess(" 42 ") == (True, 42, None)


def test_parse_guess_rejects_empty_or_non_whole_number():
    for raw_guess in ("", "4.2", "abc"):
        ok, guess, error = parse_guess(raw_guess)

        assert ok is False
        assert guess is None
        assert error


def test_difficulty_ranges_get_harder():
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    assert (easy_low, normal_low, hard_low) == (1, 1, 1)
    assert easy_high < normal_high <= hard_high
    assert get_range_for_difficulty("Unknown") == get_range_for_difficulty("Normal")


def test_attempt_limits_by_difficulty():
    assert get_attempt_limit("Easy") == 6
    assert get_attempt_limit("Normal") == 8
    assert get_attempt_limit("Hard") == 5
    assert get_attempt_limit("Unknown") == 8


def test_update_score_rewards_fast_wins_and_penalizes_misses():
    first_try_score = update_score(0, "Win", 1)
    late_win_score = update_score(0, "Win", 20)

    assert first_try_score > late_win_score
    assert late_win_score >= 10
    assert update_score(20, "Too High", 2) < 20
    assert update_score(20, "Too Low", 3) < 20
    assert update_score(20, "Invalid", 3) == 20


def test_reset_game_state_clears_round_data():
    state = {
        "secret": 12,
        "attempts": 4,
        "score": 50,
        "status": "lost",
        "history": [1, 2, 3, 4],
        "difficulty": "Easy",
    }

    reset_game_state(state, secret=150, difficulty="Hard")

    assert state == {
        "secret": 150,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
        "difficulty": "Hard",
    }
