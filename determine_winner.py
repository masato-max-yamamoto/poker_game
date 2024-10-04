import itertools

CARD_RANKS = "23456789TJQKA"


def card_index(card: str) -> int:
    return CARD_RANKS.find(card[0])


def hand_strength(hand: str) -> tuple:
    groups = sorted(((hand.count(rank), rank) for rank in set(hand)), reverse=True)
    count_vals = [count for count, _ in groups]

    if count_vals == [4, 1]:
        primary, kicker = groups[0][1], groups[1][1]
        return (7, card_index(primary), card_index(kicker))  # Four of a Kind
    elif count_vals == [3, 2]:
        primary, secondary = groups[0][1], groups[1][1]
        return (6, card_index(primary), card_index(secondary))  # Full House
    elif len(set(card[1] for card in hand)) == 1:
        return (5,) + tuple(card_index(rank) for _, rank in groups)  # Flush
    elif "".join(card[0] for card in hand) in "AKQJT98765432":
        return (4,) + tuple(card_index(rank) for _, rank in groups)  # Straight
    elif "A5432" in "".join(card[0] for card in hand):
        return (4, 3, 2, 1, 0, -1)  # Straight
    elif count_vals == [3, 1, 1]:
        primary, kicker1, kicker2 = groups[0][1], groups[1][1], groups[2][1]
        return (
            3,
            card_index(primary),
            card_index(kicker1),
            card_index(kicker2),
        )  # Three of a Kind
    elif count_vals == [2, 2, 1]:
        primary1, primary2, kicker = groups[0][1], groups[1][1], groups[2][1]
        return (
            2,
            card_index(primary1),
            card_index(primary2),
            card_index(kicker),
        )  # Two Pair
    elif count_vals == [2, 1, 1, 1]:
        primary, kicker1, kicker2, kicker3 = (
            groups[0][1],
            groups[1][1],
            groups[2][1],
            groups[3][1],
        )
        return (
            1,
            card_index(primary),
            card_index(kicker1),
            card_index(kicker2),
            card_index(kicker3),
        )  # One Pair
    else:
        return (0,) + tuple(card_index(rank) for _, rank in groups)  # High Card


def best_hand(cards: str) -> str:
    return max(
        itertools.combinations(cards, 5), key=lambda hand: hand_strength(hand)[0]
    )


def format_hand(hand: str) -> str:
    hand_str = ",".join(card[0] + card[1] for card in hand)
    return f"({hand_str})"


def determine_winner(player_hand: str, computer_hand: str, community_cards: str) -> str:
    player_best = best_hand(player_hand + community_cards)
    computer_best = best_hand(computer_hand + community_cards)

    player_strength = hand_strength(player_best)
    computer_strength = hand_strength(computer_best)

    if player_strength > computer_strength:
        result = "player"
    elif player_strength < computer_strength:
        result = "computer"
    else:
        result = "tie"

    print(f"player: {format_hand(player_best)}: {player_strength}")
    print(f"computer: {format_hand(computer_best)}: {computer_strength}")
    return result


if __name__ == "__main__":
    player_hand = ["AH", "KH"]
    computer_hand = ["QH", "QD"]
    community_cards = ["JH", "TH", "9H", "8H", "7H"]

    result = determine_winner(player_hand, computer_hand, community_cards)
    print(f"The winner is: {result}")
