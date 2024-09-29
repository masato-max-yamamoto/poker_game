# computer's actions


import itertools
import random
from collections import Counter


def simulate_holdem(
    hole_cards,
    community_cards,
    current_bet,
    raised_chip,
    pot,
    num_opponents: int = 1,
    num_trials: int = 3000,
):
    deck = [
        r + s
        for r in "23456789TJQKA"
        for s in "shdc"
        if r + s not in hole_cards + community_cards
    ]

    def hand_strength(hand: str):
        hand = sorted(hand, key=lambda x: "23456789TJQKA".index(x[0]), reverse=True)
        counts = Counter([card[0] for card in hand])
        count_vals = list(reversed(sorted(counts.values())))
        groups = sorted(
            list(counts.items()),
            key=lambda x: (x[1], "23456789TJQKA".index(x[0])),
            reverse=True,
        )
        if len(set([card[1] for card in hand])) == 1 and "AKQJT" in "".join(
            [card[0] for card in hand]
        ):
            return (9,) + tuple("23456789TJQKA".index(r) for r, _ in groups)
        elif (
            len(set([card[1] for card in hand])) == 1
            and "".join([card[0] for card in hand]) in "AKQJT98765432"
        ):
            return (8,) + tuple("23456789TJQKA".index(r) for r, _ in groups)
        elif count_vals == [4, 1]:
            primary, kicker = groups[0][0], groups[1][0]
            return (7, "23456789TJQKA".index(primary), "23456789TJQKA".index(kicker))
        elif count_vals == [3, 2]:
            primary, secondary = groups[0][0], groups[1][0]
            return (6, "23456789TJQKA".index(primary), "23456789TJQKA".index(secondary))
        elif len(set([card[1] for card in hand])) == 1:
            return (5,) + tuple("23456789TJQKA".index(r) for r, _ in groups)
        elif "".join([card[0] for card in hand]) in "AKQJT98765432":
            return (4,) + tuple("23456789TJQKA".index(r) for r, _ in groups)
        elif "A5432" in "".join([card[0] for card in hand]):
            return (4, 3, 2, 1, 0, -1)
        elif count_vals == [3, 1, 1]:
            primary, kicker1, kicker2 = groups[0][0], groups[1][0], groups[2][0]
            return (
                3,
                "23456789TJQKA".index(primary),
                "23456789TJQKA".index(kicker1),
                "23456789TJQKA".index(kicker2),
            )
        elif count_vals == [2, 2, 1]:
            primary1, primary2, kicker = groups[0][0], groups[1][0], groups[2][0]
            return (
                2,
                "23456789TJQKA".index(primary1),
                "23456789TJQKA".index(primary2),
                "23456789TJQKA".index(kicker),
            )
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
            )
        else:
            return (0,) + tuple("23456789TJQKA".index(r) for r, _ in groups)

    def best_hand(cards):
        return max(itertools.combinations(cards, 5), key=hand_strength)

    def trial() -> bool:
        random.shuffle(deck)
        my_cards = hole_cards + community_cards + deck[: 5 - len(community_cards)]
        my_best_hand = best_hand(my_cards)
        opponent_hands = [
            deck[i : i + 2]
            for i in range(
                5
                - len(
                    community_cards,
                ),
                5 - len(community_cards) + 2 * num_opponents,
                2,
            )
        ]
        opponent_best_hands = [
            best_hand(
                opponent_hand + community_cards + deck[: 5 - len(community_cards)]
            )
            for opponent_hand in opponent_hands
        ]
        num_better_hands = sum(
            1
            for opponent_best_hand in opponent_best_hands
            if hand_strength(opponent_best_hand) > hand_strength(my_best_hand)
        )
        return num_better_hands == 0

    num_wins = sum(1 for _ in range(num_trials) if trial())
    odds = num_wins / num_trials
    desired_bet = int(odds * pot / (1 - odds)) - (current_bet - raised_chip)
    return desired_bet


def computer_handler(
    raised, current_bet, raised_chip, computer_chips, pot, hole_cards, community_cards
):
    if not raised:
        desired_bet = simulate_holdem(hole_cards, community_cards, 0, 0, pot)
        if desired_bet < pot / 2:
            behavior = "c"
        elif desired_bet >= pot / 2 and desired_bet < computer_chips:
            behavior = desired_bet
        else:
            behavior = "a"

    if raised:
        desired_bet = simulate_holdem(
            hole_cards, community_cards, current_bet, raised_chip, pot
        )
        if desired_bet < raised_chip:
            behavior = "f"
        elif desired_bet >= raised_chip and desired_bet < current_bet + raised_chip:
            behavior = "c"
        elif desired_bet >= current_bet + raised_chip and desired_bet < computer_chips:
            behavior = desired_bet
        else:
            behavior = "a"
    return behavior
