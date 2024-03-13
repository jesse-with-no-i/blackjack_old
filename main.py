from bjHeader import Deck, Card, Player, Dealer, Game
from consoleGame import ConsoleGame
from GUI import GUI


def game_start(gameMode, game):
    if gameMode == "console":
        ui = ConsoleGame()

    else:
        ui = GUI(game)


def main():
    # extract the amount of money stored in "playerbank.txt"
    with open('playerBank.txt', 'r') as file:
        bank = int(file.readline())

    # create objects for the game
    deck = Deck()
    player = Player(bank)
    dealer = Dealer()
    game = Game(player, dealer, deck)

    # initiate the game
    game_start("gui", game)


if __name__ == '__main__':
    main()
