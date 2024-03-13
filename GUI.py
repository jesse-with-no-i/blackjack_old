import tkinter as tk
from tkinter import messagebox



BGCOLOR = "#CCCCFF"
BTNCOLOR = "#Dfb5fb"
CARDCOLOR = "#Fbb5c4"


class GUI():
    def __init__(self, game):
        self.game = game
        self.playerTotal = 0
        self.dealerTotal = 0

        # creates the window for the menu
        self.root = tk.Tk()
        self.root.title("Black Jack Menu")
        self.root.geometry("400x400+500+150")
        self.root.configure(bg=BGCOLOR)

        # bank label
        self.bankLabel = tk.Label(self.root, bg=BGCOLOR, text='', font=("Arial", 12))

        # create a paused variable
        self.paused = tk.BooleanVar()
        self.paused.set(True)

        # label at the top that welcomes the player to the menu
        welcomeLabel = tk.Label(self.root, bg=BGCOLOR, text="Menu:", font=("Arial", 18))
        welcomeLabel.pack(padx=10, pady=10)

        # update how much money the player has in the bank
        self.game.get_player().update_bank("playerBank.txt")

        # label that shows how much money is saved in the bank
        self.bankLabel.config(text=f"You have ${self.game.get_player().get_bank()} in the bank")
        self.bankLabel.pack(padx=10, pady=10)

        # frame containing the start button and the bet spinbox
        startFrame = tk.Frame(self.root, bg=BGCOLOR, bd=5)

        # bet label
        betLabel = tk.Label(startFrame, text="Bet:", font=("Arial", 12), bg=BGCOLOR)
        betLabel.grid(row=0, column=1)

        # player chooses what bet they want to place
        defaultBet = tk.IntVar()
        defaultBet.set(50)
        betSpinbox = tk.Spinbox(startFrame, from_=10, to=self.game.get_player().get_bank(),
                                width=4, textvariable=defaultBet)
        betSpinbox.grid(row=1, column=1, padx=2)

        # button to start over ($150 in the bank)
        startButton = tk.Button(startFrame, bg=BTNCOLOR, text='Start Game', font=('Arial', 14), width=16,
                                   command=lambda: self.on_start(betSpinbox))
        startButton.grid(rowspan=2, row=0, column=0)

        # place the start frame into the menu
        startFrame.pack(padx=10, pady=10)

        # button to reset bank information
        resetBankButton = tk.Button(self.root, bg=BTNCOLOR, text='Restart with $150', font=('Arial', 14), width=20,
                                    command=self.reset_bank)
        resetBankButton.pack(padx=10, pady=10)

        # button to exit
        exitButton = tk.Button(self.root, bg=BTNCOLOR, text='Exit', font=('Arial', 14), width=20,
                               command=self.on_close)
        exitButton.pack(padx=10, pady=10)

        # decides what to do when closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # displays the main window on screen
        self.root.mainloop()


    def reset_bank(self):
        # ask if the player really wants to reset their progress
        if messagebox.askyesno(title="Reset bank?", message="Do you really want to reset?\n"
                                                            "You will have $150 in the bank."):

            with open('playerBank.txt', 'w') as file:

                # overwrite the bank text file to be 150
                file.write("150")
                file.close()

            # update the amount of money in the player's bank
            player = self.game.get_player()
            player.update_bank("playerBank.txt")

            # update the old label
            self.bankLabel.config(text=f"You have ${self.game.get_player().get_bank()} in the bank")


    def on_start(self, betSpinbox):
        bet = int(betSpinbox.get())

        # flag variable
        validInput = True

        # validate the user input

        # check if the bet is too high
        if bet > self.game.get_player().get_bank():
            messagebox.showinfo(message="Sorry, you don't have enough money to place your bet.")
            validInput = False

        # check if the bet is too low
        elif bet < 10:
            messagebox.showinfo(message="Sorry, your bet is lower than the minimum bet of $10.")
            validInput = False


        if not validInput:

            # end the program
            self.root.destroy()

            return



        # deal the first two cards to each player
        self.game.deal_cards()

        # set the bet to whatever is read from the bet spinbox
        self.game.set_bet(bet)

        # hide the menu
        self.root.withdraw()

        # create window where game is played
        self.create_game_window()


    def on_close(self):
        if messagebox.askyesno(title="Exit?", message="Do you really want to Exit?"):
            self.root.destroy()


    # creates a window for the game to be played in
    def create_game_window(self, dealer=False):
        gameWindow = tk.Tk()
        gameWindow.title("Black Jack")
        gameWindow.geometry("400x700+500+20")
        gameWindow.configure(bg=BGCOLOR)


        # label showing how much money you have in the bank
        bankLabelText = f"You have ${self.game.get_player().get_bank()} in the bank"
        bankLabel = tk.Label(gameWindow, bg=BGCOLOR, text=bankLabelText, font=("Arial", 12))
        bankLabel.pack(padx=10, pady=10)

        # create a frame where the players cards will appear
        playerFrame = tk.Frame(gameWindow, bg=BGCOLOR, bd=5)

        # label "your hand"
        yourHandLabel = tk.Label(gameWindow, text="Your Hand", font=("Arial", 14), bg=BGCOLOR)
        yourHandLabel.pack(pady=10)

        # gets each card
        for c in self.game.get_player().get_hand():
            cardText = f"{c.get_name()} of {c.get_suit()}"
            cardLabel = tk.Label(playerFrame, text=cardText, font=("Arial", 12), width=16, bg=CARDCOLOR)
            cardLabel.pack(padx=10, pady=2)

        playerFrame.pack(pady=10)

        # create frame where dealer's cards will appear
        dealerFrame = tk.Frame(gameWindow, bg=BGCOLOR, bd=5)

        # label for the dealer's hand
        # only show the second card
        c = self.game.get_dealer().get_hand()[1]
        cardText = f"{c.get_name()} of {c.get_suit()}"
        cardLabel = tk.Label(dealerFrame, text=cardText, font=("Arial", 12), width=16, bg=CARDCOLOR)
        cardLabel.pack(padx=10, pady=2)

        # place a label saying that this is the dealer's hand
        dealerHandLabel = tk.Label(gameWindow, text="Dealer Shows:", font=('Aria', 14), bg=BGCOLOR)
        dealerHandLabel.pack(pady=10)

        # place the frame that shows the dealer's cards
        dealerFrame.pack(pady=10)

        # frame containing the buttons to hit or stand
        buttonFrame = tk.Frame(gameWindow, bg=BGCOLOR, bd=5)

        # create the buttons to hit or stand
        buttonHit = tk.Button(buttonFrame, bg=BTNCOLOR, text='Hit', font=('Arial', 14), width=10,
                              command=lambda: self.player_hit(gameWindow, buttonNext, buttonHit, buttonStand, playerFrame))
        buttonStand = tk.Button(buttonFrame, bg=BTNCOLOR, text='Stand', font=('Arial', 14), width=10,
                                command=lambda: self.player_stand(dealerFrame, buttonHit, buttonStand, buttonNext, gameWindow))

        # in the frame, have the buttons on a grid
        buttonHit.grid(row=0, column=0)
        buttonStand.grid(row=0, column=1)

        # place the button frame in the window
        buttonFrame.pack(pady=10)

        # if it is the dealer's turn, create a "next" button so execution pauses until the button is pressed
        buttonNext = tk.Button(gameWindow, bg=BTNCOLOR, text='Next', font=('Arial', 14), width=10,
                               command=lambda: self.paused.set(False))

        # what to do when closing the window
        gameWindow.protocol("WM_DELETE_WINDOW", lambda: self.close_game_window(gameWindow))


    def player_hit(self, window, buttonNext, buttonHit, buttonStand, playerFrame):
        # get the player from the game
        player = self.game.get_player()

        # player hits from the game deck
        player.hit(self.game.get_deck())

        # check if the player's total is greater than 21
        if player.get_total() > 21:

            # if the player has aces, subtract 10 from the total
            # it doesn't matter which card's value is decreased, so we choose the first card
            card = player.get_hand()[0]
            if player.get_num_aces() > 0:

                # subtract 10 from the value of the first card
                card.set_value(card.get_value() - 10)
                # keep track of used aces
                player.remove_ace()

                # update the contents of playerFrame
                c = self.game.get_player().get_hand()[-1]
                cardText = f"{c.get_name()} of {c.get_suit()}"
                cardLabel = tk.Label(playerFrame, text=cardText, font=("Arial", 12), width=16, bg=CARDCOLOR)
                cardLabel.pack(padx=10, pady=2)

                return

            # if the total is greater than 21 but there are no aces, it is a bust
            else:
                self.player_bust(window, buttonNext, buttonHit, buttonStand, playerFrame)

                return

        # otherwise update the players cards
        c = self.game.get_player().get_hand()[-1]
        cardText = f"{c.get_name()} of {c.get_suit()}"
        cardLabel = tk.Label(playerFrame, text=cardText, font=("Arial", 12), width=16, bg=CARDCOLOR)
        cardLabel.pack(padx=10, pady=2)


    def player_stand(self, dealerFrame, buttonHit, buttonStand, buttonNext, gameWindow):
        # self.playerTotal = self.game.get_player_total()
        #
        # # get rid of the old window before creating a new one
        # if window.winfo_exists():
        #     window.destroy()
        # self.create_game_window(dealer=True)

        c = self.game.get_dealer().get_hand()[0]
        cardText = f"{c.get_name()} of {c.get_suit()}"
        cardLabel = tk.Label(dealerFrame, text=cardText, font=("Arial", 12), width=16, bg=CARDCOLOR)
        cardLabel.pack(padx=10, pady=2)

        buttonHit.config(state='disabled')
        buttonStand.config(state='disabled')

        buttonNext.pack(pady=5)

        # wait before each turn until the next button is pressed
        self.root.wait_variable(self.paused)

        # and if after the window is set up for the dealer, call the function to start dealer's turn
        self.dealer_turn(dealerFrame, gameWindow)


    def player_bust(self, window, buttonNext, buttonHit, buttonStand, playerFrame):

        # display the last card that was drawn
        c = self.game.get_player().get_hand()[len(self.game.get_player().get_hand())-1]
        cardText = f"{c.get_name()} of {c.get_suit()}"
        cardLabel = tk.Label(playerFrame, text=cardText, font=("Arial", 12), width=16, bg=CARDCOLOR)
        cardLabel.pack(padx=10, pady=2)

        # place the next button on screen
        buttonNext.pack(pady=5)

        # disable other buttons
        buttonHit.config(state='disabled')
        buttonStand.config(state='disabled')

        # pause the game until the next button is pressed
        self.root.wait_variable(self.paused)

        # destroy the old window
        if window.winfo_exists():
            window.destroy()

        # reset the game
        self.game.reset_game(self.game.get_player().get_bank())

        # bring up the menu again
        self.root.deiconify()

        # call the lose function
        self.lose()


    def close_game_window(self, window):
        # close the game window and bring up the menu again

        # first check if the window exists
        if window.winfo_exists():
            window.destroy()

        self.root.deiconify()

        # make sure the game is reset before the next game
        self.game.reset_game(self.game.get_player().get_bank())


    def dealer_turn(self, cardFrame, window):
        # get the dealer from the game
        dealer = self.game.get_dealer()
        # get player from the game
        player = self.game.get_player()

        # begin a loop
        # dealer will hit if their total is less than 17, stand otherwise
        while dealer.get_total() < 17:
            dealer.hit(self.game.get_deck())

            # update the window by placing the new card in the frame
            # c is the last card the dealer drew
            c = dealer.get_hand()[-1]
            cardText = f"{c.get_name()} of {c.get_suit()}"
            cardLabel = tk.Label(cardFrame, text=cardText, font=("Arial", 12), width=16, bg=CARDCOLOR)
            cardLabel.pack(padx=10, pady=2)

            # check if the dealer busts
            if dealer.get_total() > 21:
                # also check if the dealer has any aces
                card = dealer.get_hand()[0]
                if dealer.get_num_aces() > 0:

                    # if the dealer does have aces, subtract ten and check if they are still at 16 or less
                    card.set_value(card.get_value() - 10)
                    dealer.remove_ace()

                    # this goes back to the beginning of the while loop
                    continue

                # if the total is more than 21 and there are no aces, player wins
                else:
                    self.win()
                    self.close_game_window(window)
                    return

        # if the dealer stops, compare with the player's cards to determine if they win or lose (or tie)
        # also destroy the game window after showing the result
        if player.get_total() > dealer.get_total():
            self.win()
            self.close_game_window(window)

        elif player.get_total() == dealer.get_total():
            self.tie()
            self.close_game_window(window)

        else:
            self.lose()
            self.close_game_window(window)


    def win(self):
        messagebox.showinfo(title="Winner!", message="Congratulations! You won!")

        # determine how much money is now in the bank
        newBank = self.game.get_player().get_bank() + self.game.get_bet()

        # add funds to the player bank
        with open('playerBank.txt', 'w') as file:
            # overwrite the bank text file to be 150
            file.write(str(newBank))
            file.close()

        # update player's bank with the new bank total
        self.game.get_player().update_bank("playerBank.txt")

        # update the bank label with the new info
        self.bankLabel.config(text=f"You have ${self.game.get_player().get_bank()} in the bank")

        # go back to menu
        self.root.deiconify()


    def lose(self):
        messagebox.showinfo(title="You lose!", message="Sorry, you lost!")

        # determine how much money is now in the bank
        newBank = self.game.get_player().get_bank() - self.game.get_bet()

        # subtract funds from the player bank
        with open('playerBank.txt', 'w') as file:
            # overwrite the bank text file to be 150
            file.write(str(newBank))
            file.close()

        # update player's bank with the new bank total
        self.game.get_player().update_bank("playerBank.txt")

        # update the bank label with the new info
        self.bankLabel.config(text=f"You have ${self.game.get_player().get_bank()} in the bank")

        # bring back the menu
        self.root.deiconify()


    def tie(self):
        messagebox.showinfo(title="Tie", message="It's a push! You tied with the dealer.")

        # bring back the menu
        self.root.deiconify()
