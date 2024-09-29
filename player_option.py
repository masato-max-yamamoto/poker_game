# require a plyer to take an action
import math


def first_option(computer_behavior: str, bet_amount: int, player_chips: int, pot: int):
    if computer_behavior == "check":
        player_bet = input(
            f"your turn: check(c), all-in(a), or bet? if bet, give the bet amount: {math.ceil(pot / 2)} - {player_chips}"
        )
    elif bet_amount * 2 < player_chips:
        player_bet = input(
            f"your turn: call(c), fold(f), or raise? if raise. give the bet amount: {bet_amount * 2} - {player_chips -1}"
        )
    else:
        player_bet = input("your turn: call(c), all-in(a) or fold(f)")

    while True:
        try:
            if player_bet in ["c", "f", "a"]:
                break
            else:
                player_bet = int(player_bet)
                if player_bet < bet_amount * 2 or player_bet > player_chips - 1:
                    raise ValueError
            break
        except ValueError:
            if computer_behavior == "c":
                player_bet = input(
                    f"error: give check(c), all-in(a), or the bet amount: {math.ceil(pot / 2)} - {player_chips}"
                )
            elif bet_amount * 2 < player_chips:
                player_bet = input(
                    f"error: give call(c), fold(f), or the bet amount: {bet_amount * 2} - {player_chips - 1}"
                )
            else:
                player_bet = input("error: give call(c), all-in(a), or fold(f)")
    return player_bet


def option_to_reraise(new_bet, player_bet, player_chips, errored):
    if not errored:
        if new_bet * 2 < player_bet + player_chips:
            raised_player_bet = input(
                f"your turn: call(c), fold(f), or raise? if raise, give the bet amount: {new_bet * 2} - {player_bet + player_chips -1}"
            )
        else:
            raised_player_bet = input("your turn: call(c), all-in(a), or fold(f)")
    else:
        if new_bet * 2 < player_bet + player_chips:
            raised_player_bet = input(
                f"error: give call(c), fold(f), or the bet amount: {new_bet * 2} - {player_bet + player_chips -1}"
            )
        else:
            raised_player_bet = input("error: give call(c), all-in(a), or fold(f)")

    return raised_player_bet


def option_to_allin():
    player_bet = input("your turn: all-in(a) or fold(f)")

    while True:
        if player_bet not in ["a", "f"]:
            player_bet = input("error: give all-in(a) or fold(f)")
        else:
            break
    return player_bet
