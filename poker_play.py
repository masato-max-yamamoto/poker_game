import random

from determine_winner import determine_winner
from odds_calculate import computer_handler
from player_option import first_option, option_to_allin, option_to_reraise

suits = ["H", "D", "C", "S"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + self.suit


def create_deck() -> list:
    deck = [Card(suit, rank) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


def deal_hands(deck: list) -> tuple:
    player_hand = [deck.pop(), deck.pop()]
    computer_hand = [deck.pop(), deck.pop()]
    return player_hand, computer_hand


def deal_community_cards(deck: list) -> list:
    return [deck.pop() for _ in range(5)]


def show_hands(
    player_hand: list, community_cards: list, revealed: int, computer_hand: list = None
):
    print(f"your hand: {', ' .join(str(card) for card in player_hand)}")
    print(
        f"community cards: {', ' .join(str(card) if i < revealed else "X" for i, card in enumerate(community_cards))}"
    )
    if computer_hand:
        print(f"computer hand: {', ' .join(str(card) for card in computer_hand)}")
    else:
        print("computer hand is unrevealed ")


def betting_round(player_chips, computer_chips, pot, game_over, folder):
    # bettings by a computer
    if pot == 0:  # pre-flop
        bet_amount = 10
        print(f"computer bets {bet_amount}")
        computer_behavior = 10
    else:
        computer_behavior = computer_handler(
            False, 0, 0, computer_chips, pot, computer_hand_str, community_cards_str
        )
        if computer_behavior == "c":
            bet_amount = 0
            print("computer checks")
        elif computer_behavior == "a":
            bet_amount = computer_chips
            print(f"computer goes all-in with {bet_amount}")
        else:
            bet_amount = computer_behavior
            print(f"computer bets {bet_amount}")
    computer_chips -= bet_amount
    pot = bet_amount
    print(f"pot: {pot}")

    raised = False
    player_bet = first_option(computer_behavior, bet_amount, player_chips, pot)

    if player_bet == "f":  # player's fold
        computer_chips += pot
        pot = 0
        game_over = True
        folder = "player"
        print("you fold, computer wins")
        return player_chips, computer_chips, pot, game_over, folder
    elif player_bet == "a":  # player's all-in
        pot += player_chips
        player_chips = 0
        current_bet = pot - bet_amount
        print("you went all-in")

        computer_behavior = computer_handler(
            False, 0, 0, computer_chips, pot, computer_hand_str, community_cards_str
        )
        if computer_behavior != "f":
            computer_behavior = "a"

        if computer_behavior == "f":
            player_chips += pot
            pot = 0
            game_over = True
            folder = "computer"
            print("computer folds, you win")
            return player_chips, computer_chips, pot, game_over, folder
        else:
            pot += computer_chips
            computer_chips = 0
            game_over = True
            print("computer went all-in")
            return player_chips, computer_chips, pot, game_over, folder

    elif player_bet == "c":  # check or call
        player_chips -= bet_amount
        pot += bet_amount
        print("you called. next round")
        return player_chips, computer_chips, pot, game_over, folder

    else:  # player raises
        player_chips -= player_bet
        pot += bet_amount
        print(f"you raised {player_bet}")
        raise_amount = player_bet - bet_amount
        raised = True
        # computer's turn
        while raised:
            computer_behavior = computer_handler(
                True,
                player_bet,
                bet_amount,
                computer_chips,
                pot,
                computer_hand_str,
                community_cards_str,
            )
            if computer_behavior == "f":
                player_chips += pot
                pot = 0
                game_over = True
                folder = "computer"
                print("computer folds, you won")
                break
            elif computer_behavior == "c":
                computer_chips -= raise_amount
                pot += raise_amount
                print("computer calls")
                break
            elif computer_behavior == "a":
                pot -= computer_chips
                computer_chips = 0
                print("computer went all-in")

                player_bet = option_to_allin()
                if player_bet == "a":
                    pot += player_chips
                    player_chips = 0
                    game_over = True
                    print("you went all-in")
                    break
                else:
                    computer_chips += pot
                    pot = 0
                    game_over = True
                    folder = "player"
                    print("you fold, computer wins")
                    break
            else:  # re-raise
                new_bet = computer_behavior
                computer_chips -= new_bet - bet_amount
                pot += new_bet - bet_amount
                bet_amount = new_bet
                print(f"computer raised {new_bet}")
                raised_player_bet = option_to_reraise(
                    new_bet, player_bet, player_chips, False
                )

                while True:
                    try:
                        if raised_player_bet == "a":
                            pot += player_chips
                            current_bet = player_bet + player_chips
                            player_chips = 0
                            print("you went all-in")
                            computer_behavior = computer_handler(
                                True,
                                current_bet,
                                raise_amount,
                                computer_chips,
                                pot,
                                computer_hand_str,
                                community_cards_str,
                            )
                            if computer_behavior != "f":
                                computer_behavior = "a"

                            if computer_behavior == "f":
                                player_chips += pot
                                pot = 0
                                game_over = True
                                folder = "computer"
                                print("computer folds, you win")
                            else:
                                pot += computer_chips
                                computer_chips = 0
                                game_over = True
                                print("computer went all-in")

                            break
                        elif raised_player_bet == "f":
                            computer_chips += pot
                            pot = 0
                            game_over = True
                            folder = "player"
                            print("you fold, computer wins")
                            break
                        elif raised_player_bet == "c":
                            player_chips -= raise_amount
                            pot += raise_amount
                            print("you call")
                            break

                        else:
                            raised_player_bet = int(raised_player_bet)
                            if (
                                raised_player_bet < new_bet * 2
                                or raised_player_bet > player_chips - 1
                            ):
                                raise ValueError
                            else:
                                player_chips -= raised_player_bet - player_bet
                                pot += raised_player_bet - player_bet
                                player_bet = raised_player_bet
                                break
                    except ValueError:
                        raised_player_bet = option_to_reraise(
                            raise_amount, player_bet, player_chips, False
                        )
    return player_chips, computer_chips, pot, game_over, folder


def main():
    player_chips = 1000
    computer_chips = 1000
    pot = 0
    game_over = False
    folder = None
    deck = create_deck()

    global player_hand, computer_hand, community_cards, revealed
    player_hand, computer_hand = deal_hands(deck)
    community_cards = deal_community_cards(deck)

    global player_hand_str, computer_hand_str, community_cards_str
    player_hand_str = [str(card) for card in player_hand]
    computer_hand_str = [str(card) for card in computer_hand]
    full_community_cards_str = [str(card) for card in community_cards]

    print("pre-flop betting round")
    revealed = 0
    community_cards_str = full_community_cards_str[:revealed]
    show_hands(player_hand, community_cards, revealed)
    player_chips, computer_chips, pot, game_over, folder = betting_round(
        player_chips, computer_chips, pot, game_over, folder
    )
    if not game_over:
        print("flop")
        revealed = 3
        community_cards_str = full_community_cards_str[:revealed]
        show_hands(player_hand, community_cards, revealed)
        player_chips, computer_chips, pot, game_over, folder = betting_round(
            player_chips, computer_chips, pot, game_over, folder
        )

    if not game_over:
        print("turn")
        revealed = 4
        community_cards_str = full_community_cards_str[:revealed]
        show_hands(player_hand, community_cards, revealed)
        player_chips, computer_chips, pot, game_over, folder = betting_round(
            player_chips, computer_chips, pot, game_over, folder
        )

    if not game_over:
        print("river")
        revealed = 5
        community_cards_str = full_community_cards_str[:revealed]
        show_hands(player_hand, community_cards, revealed)
        player_chips, computer_chips, pot, game_over, folder = betting_round(
            player_chips, computer_chips, pot, game_over, folder
        )

    if folder is None:
        print("showdown")
        revealed = 5
        show_hands(player_hand, community_cards, revealed, computer_hand)
    else:
        print("no showdown")

    if folder is None:
        result = determine_winner(
            player_hand_str, computer_hand_str, community_cards_str
        )
        print(result)
        if result == "player":
            player_chips += pot
            pot = 0
        elif result == "computer":
            computer_chips += pot
            pot = 0
        else:
            player_chips += pot // 2
            computer_chips += pot // 2
            pot = 0

    print(f"player's chips: {player_chips}, computer's chips: {computer_chips}")


if __name__ == "__main__":
    main()
