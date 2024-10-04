# require a plyer to take an action
import math


def get_player_input(prompt: str, valid_options: list = None) -> str:
    while True:
        player_input = input(prompt)
        if valid_options and player_input in valid_options:
            return player_input
        try:
            player_input = int(player_input)
            return player_input
        except ValueError:
            pass
        print("Invalid input. Please try again.")


def validate_bet(player_bet, min_bet, max_bet):
    return (
        isinstance(player_bet, int) and min_bet <= player_bet <= max_bet
    ) or isinstance(player_bet, str)


def first_option(computer_behavior: str, bet_amount: int, player_chips: int, pot: int):
    if computer_behavior == "c":
        prompt = f"your turn: check(c), all-in(a), or bet? if bet, give the bet amount: {math.ceil(pot / 2)} - {player_chips}"
        valid_options = ["c", "a"]
    elif bet_amount * 2 < player_chips:
        prompt = f"your turn: call(c), fold(f), or raise? if raise, give the bet amount: {bet_amount * 2} - {player_chips - 1}"
        valid_options = ["c", "f"]
    else:
        prompt = "your turn: call(c), all-in(a) or fold(f)"
        valid_options = ["c", "a", "f"]

    player_bet = get_player_input(prompt, valid_options)

    while not validate_bet(player_bet, bet_amount * 2, player_chips - 1):
        if computer_behavior == "c":
            prompt = f"error: give check(c), all-in(a), or the bet amount: {math.ceil(pot / 2)} - {player_chips}"
        elif bet_amount * 2 < player_chips:
            prompt = f"error: give call(c), fold(f), or the bet amount: {bet_amount * 2} - {player_chips - 1}"
        else:
            prompt = "error: give call(c), all-in(a), or fold(f)"
        player_bet = get_player_input(prompt, valid_options)

    return player_bet


def option_to_reraise(new_bet, player_bet, player_chips, errored):
    if new_bet * 2 < player_bet + player_chips:
        prompt = f"your turn: call(c), fold(f), or raise? if raise, give the bet amount: {new_bet * 2} - {player_bet + player_chips - 1}"
        error_prompt = f"error: give call(c), fold(f), or the bet amount: {new_bet * 2} - {player_bet + player_chips - 1}"
    else:
        prompt = "your turn: call(c), all-in(a), or fold(f)"
        error_prompt = "error: give call(c), all-in(a), or fold(f)"

    if errored:
        prompt = error_prompt

    valid_options = ["c", "a", "f"]
    raised_player_bet = get_player_input(prompt, valid_options)
    return raised_player_bet


def option_to_allin():
    prompt = "your turn: all-in(a) or fold(f)"
    error_prompt = "error: give all-in(a) or fold(f)"
    valid_options = ["a", "f"]

    player_bet = get_player_input(prompt, valid_options)
    while player_bet not in valid_options:
        player_bet = get_player_input(error_prompt, valid_options)
    return player_bet


if __name__ == "__main__":
    print(get_player_input("enter the text:", ["a", "b", "c"]))
