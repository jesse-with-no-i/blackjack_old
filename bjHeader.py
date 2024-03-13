from random import randint

NAMES = ['Ace', '2', '3', '4',
         '5', '6', '7', '8', '9',
         '10', 'Jack', 'Queen', 'King']

VALUES = [11, 2, 3, 4,
          5, 6, 7, 8, 9,
          10, 10, 10, 10]

SUITS = ["Spades", "Diamonds", "Clubs", "Hearts"]

# Card class:
# Attributes:
# - name -> string
# - suit -> string
# - value -> int
# Methods:
# - set_name, set_suit, set_value
# - get_name, get_suit, get_value
# - Constructors -> default and parameterized
class Card:
    # constructor:
    # - creates a card using the inputted values
    def __init__(self, name='', suit='', value=0, image="image/card_back.png"):
        self.name = name
        self.suit = suit
        self.value = value
        self.image = image


    # getters and setters for each attribute
    def set_name(self, name):
        self.name = name


    def set_suit(self, suit):
        self.suit = suit


    def set_value(self, value):
        self.value = value


    def set_image(self, image):
        self.image = image


    def get_name(self):
        return self.name


    def get_suit(self):
        return self.suit


    def get_value(self):
        return self.value


    def get_image(self):
        return self.image


    # Input:
    # - none
    # Output:
    # - none
    # Side-effects:
    # - card information is printed
    def print_info(self):
        print('Name:', self.name, '\nSuit:', self.suit, '\nValue:', self.value, '\n')


# Deck class:
# Attributes:
# - Cards -> [Card]
# Methods:
# - default constructor
# - draw_card() -> returns a random card and removes it from the deck
# - get_card(card) -> returns the specified card, gives error if it does not exist
# - remove_card(card) -> deletes the specified card from the deck
# - add_cards(cards) -> adds the cards from a list of cards into the deck
# - reset() -> deletes the old list of cards and constructs the default one
# - show_deck() -> prints out the contents of cards
class Deck:
    def __init__(self):
        self.cards = []

        # loop to create a card object for each card in a deck and insert it into cards
        for n in range(len(NAMES)):
            v = VALUES[n]
            for s in SUITS:
                self.cards.append(Card(NAMES[n], s, v, self.select_image(Card(NAMES[n]), s)))
        # END OF LOOP


    # Input:
    # - list of cards
    # Output:
    # - none
    # Side-effects:
    # - deck now consists of the cards from the list of cards
    def create_custom_deck(self, cards):
        self.cards = cards


    # Input:
    # - card
    # Output:
    # - a card from the deck
    # Side-effects:
    # - cards is updated so that the card is no longer in the deck
    def get_card(self, card):
        c = self.cards[self.cards.index(card)]
        self.cards.remove(card)
        return c


    # Input:
    # - card
    # Output:
    # - none
    # Side-effects:
    # - card is no longer in deck
    def remove_card(self, card):
        try:
            self.cards.remove(card)
        except ValueError:
            print("Specified card is not in the deck")
            exit(1)


    # Input:
    # - none
    # Output:
    # - a random card from the deck
    # Side-effects:
    # - the card no longer exists in the deck#
    def draw_card(self):
        cardIndex = randint(0, len(self.cards)-1)
        return self.get_card(self.cards[cardIndex])


    # Input:
    # - a single card
    # Output:
    # - none
    # Side-effects
    # - the card is added to the deck
    def add_card(self, card):
        self.cards[len(self.cards)] = card


    # Input:
    # - list of cards
    # Output:
    # - none
    # Side-effects
    # - each card from the list of cards is added to the deck
    def add_cards(self, cards):
        for c in cards:
            self.add_card(c)

    # Input:
    # - none
    # Output:
    # - none
    # Side-effects:
    # - the deck now consists of one of each card of a regular deck of cards#
    def reset(self):
        self.cards = []

        # loop to create a card object for each card in a deck and insert it into cards
        for n in range(len(NAMES)):
            v = VALUES[n]
            for s in SUITS:
                self.cards.append(Card(NAMES[n], s, v))
        # END OF LOOP


    def show_deck(self):
        for c in self.cards:
            c.print_info()


    def get_deck(self):
        return self.cards


    def select_image(self, name, suit):
        return "images/card_back.png"


# Player class:
# Attributes:
# - hand -> list of cards
# - total -> integer representing the total value of cards
# - bank -> decimal value representing money in the bank
# Methods:
# - hit -> take a card from the deck and add it to hand
# - get_total -> gets the total of cards in hand
class Player:
    def __init__(self, bank=50):
        self.hand = []
        self.total = 0
        self.bank = bank
        self.numAces = 0


    # Input:
    # - deck object
    # Output:
    # - none
    # Side-effects:
    # - the card is removed from the deck
    # - the card is added to player's hand
    def hit(self, deck):
        self.hand.append(deck.draw_card())

        # if the newly drawn card is an ace, add to numAces
        if self.hand[-1].get_name() == "Ace":
            self.numAces += 1


    # Input:
    # - none
    # Output:
    # - integer -> total value of cards in hand
    def get_total(self):
        total = 0
        for card in self.hand:
            total += card.get_value()

        return total


    def get_hand(self):
        return self.hand


    def get_bank(self):
        return self.bank


    def get_num_aces(self):
        return self.numAces


    def remove_ace(self):
        self.numAces -= 1

    # reads the amount stored in the file and stores it in the player's bank
    def update_bank(self, filename):
        with open(filename, 'r') as file:
            line = file.readline()
            amount = int(line)
            self.bank = amount
            file.close()


# Dealer class:
# Attributes:
# - hand -> list of cards
# - total -> integer representing the total value of cards
# Methods:
# - hit -> take a card from the deck and add it to hand
# - get_total -> gets the total of cards in hand
class Dealer:
    def __init__(self):
        self.hand = []
        self.total = 0
        self.numAces = 0


    # Input:
    # - deck object
    # Output:
    # - none
    # Side-effects:
    # - the card is removed from the deck
    # - the card is added to player's hand
    def hit(self, deck):
        self.hand.append(deck.draw_card())

        # if the newly drawn card is an ace, add to numAces
        if self.hand[-1].get_name() == "Ace":
            self.numAces += 1


    # Input:
    # - none
    # Output:
    # - integer -> total value of cards in hand
    def get_total(self):
        total = 0
        for card in self.hand:
            total += card.get_value()

        return total


    def get_hand(self):
        return self.hand


    def get_num_aces(self):
        return self.numAces


    def remove_ace(self):
        self.numAces -= 1


# game class:
# Attributes:
# - player object
# - dealer object
# - deck object
# Methods:
# - #
class Game:
    def __init__(self, player=Player(), dealer=Dealer(), deck=Deck()):
        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.bet = 0


    # Input:
    # - none
    # Output:
    # - none
    # Side-effects:
    # - player has 2 cards in hand
    # - dealer has 2 cards in hand
    def deal_cards(self):
        self.player.hit(self.deck)
        self.dealer.hit(self.deck)
        self.player.hit(self.deck)
        self.dealer.hit(self.deck)


    def get_player(self):
        return self.player


    def get_dealer(self):
        return self.dealer


    def get_deck(self):
        return self.deck


    def reset_game(self, bank):
        self.player = Player(bank)
        self.dealer = Dealer()
        self.deck.reset()


    def get_player_total(self):
        return self.player.get_total()


    def get_dealer_total(self):
        return self.dealer.get_total()


    def set_bet(self, bet):
        self.bet = bet


    def get_bet(self):
        return int(self.bet)
