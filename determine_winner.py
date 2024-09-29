from collections import Counter
from itertools import combinations


def hand_strength(hand: str):
    hand = sorted(hand, key=lambda x: "23456789TJQKA".index(x[0]), reverse=True)
    counts = Counter([card[0] for card in hand])
    count_vals = list(reversed(sorted(counts.values())))
    groups = sorted(
        list(
            counts.items(),
            key=lambda x: (x[1], "23456789TJQKA".index(x[0])),
            reverse=True,
        )
    )

    if len(set([card[1] for card in hand])) == 1 and "AKQJT" in "".join(
        [card[0] for card in hand]
    ):
        return (9,) + tuple(
            "23456789TJQKA".index(r) for r, _ in groups
        )  # Royal Straight Flush
    elif (
        len(set([card[1] for card in hand])) == 1
        and "".join([card[0] for card in hand]) in "AKQJT98765432"
    ):
        return (8,) + tuple(
            "23456789TJQKA".index(r) for r, _ in groups
        )  # Straight Flush
    elif count_vals == [4, 1]:
        primary, kicker = groups[0][0], groups[1][0]
        return (
            7,
            "23456789TJQKA".index(primary),
            "23456789TJQKA".index(kicker),
        )  # Four of a Kind
    elif count_vals == [3, 2]:
        primary, secondary = groups[0][0], groups[1][0]
        return (
            6,
            "23456789TJQKA".index(primary),
            "23456789TJQKA".index(secondary),
        )  # Full House
    elif len(set([card[1] for card in hand])) == 1:
        return (5,) + tuple("23456789TJQKA".index(r) for r, _ in groups)  # Flush
    elif "".join([card[0] for card in hand]) in "AKQJT98765432":
        return (4,) + tuple("23456789TJQKA".index(r) for r, _ in groups)  # Straight
    elif "A5432" in "".join([card[0] for card in hand]):
        return (4, 3, 2, 1, 0, -1)  # Straight
    elif count_vals == [3, 1, 1]:
        primary, kicker1, kicker2 = groups[0][0], groups[1][0], groups[2][0]
        return (
            3,
            "23456789TJQKA".index(primary),
            "23456789TJQKA".index(kicker1),
            "23456789TJQKA".index(kicker2),
        )  # Three of a Kind
    elif count_vals == [2, 2, 1]:
        primary1, primary2, kicker = groups[0][0], groups[1][0], groups[2][0]
        return (
            2,
            "23456789TJQKA".index(primary1),
            "23456789TJQKA".index(primary2),
            "23456789TJQKA".index(kicker),
        )  # Two Pair
    elif count_vals == [2, 1, 1, 1]:
        primary, kicker1, kicker2, kicker3 = (
            groups[0][0],
            groups[1][0],
            groups[2][0],
            groups[3][0],
        )
        return (
            1,
            "23456789TJQKA".index(primary),
            "23456789TJQKA".index(kicker1),
            "23456789TJQKA".index(kicker2),
            "23456789TJQKA".index(kicker3),
        )  # One Pair
    else:
        return (0,) + tuple("23456789TJQKA".index(r) for r, _ in groups)  # High Card


def best_hand(cards: str) -> str:
    return max(combinations(cards, 5), key=lambda hand: hand_strength(hand)[0])


def format_hand(hand: str) -> str:
    hand_str = ",".join([card[0] + card[1] for card in hand])
    return "({})".format(hand_str)


def determine_winner(player_hand: str, computer_hand: str, community_cards: str) -> str:
    player_best = best_hand(player_hand + community_cards)
    computer_best = best_hand(computer_hand + community_cards)

    player_strength, player_hand_name = hand_strength(player_best)
    computer_strength, computer_hand_name = hand_strength(computer_best)
    if player_strength > computer_strength:
        result = "player"
    elif player_strength < computer_strength:
        result = "computer"
    else:
        result = "tie"

    print("player: {}: {}".format(format_hand(player_best), player_hand_name))  # player
    print(
        "computer: {}: {}".format(format_hand(computer_best), computer_hand_name)
    )  # computer
    return result
