from bjHeader import Deck, Card

# Objects for game:
# - game
#   - contains everything in the game
#   - allows the current player to hit or stand
#   - hit chooses a card from the deck
#   - stand saves the cards and moves on to the dealer, or ends the turn if it is the dealer
#
# - player
#   - the person playing the game
#   - has a hand (list of cards)
#   - has a total (value of cards added up)
#   - has a bank (amount of money)
#   - can draw a card
#
# - dealer
#   - like the player, but has no bank
#
# - deck
#   - a Deck object
#   - contains the cards available in the game
