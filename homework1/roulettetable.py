#-------------------------------------------------------------------------------
# Name:        RouletteTable
# Purpose:     This class allows a player (from class Player) to play Roulette
#
# Author:      Dan
#
# Created:     25.03.2015
# Copyright:   (c) Dan 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import random
import os
from player import Player

class RouletteTable:
    """ the table class - persons can bet and win/lose money"""
    def __init__(self):
        self.roulette_number = None
        self.playerOnTable = None
        self.moneyOnTable = 0

    def starting_playing(self):
        playername = raw_input("Welcome to French Terminal Roulette!\nPlease enter your name?\n")
        # if name contains numbers, then the player will be asked if it's really his name - if not then the name can be changed
        while any(c.isdigit() for c in playername):
            answer = raw_input("Is "+playername+" really your name? (y/n)").lower()
            if answer in ['yes','y','ja']:
                break
            elif answer not in ['no','n','nein']:
                print('This is not a valid answer. Please enter your real name y/n.')
            else:
                playername = raw_input("So, what is your name?")


        # set up the description for the user
        introduction = "How does French Terminal Roulette work?\n\n"
        "At the beginning you can set the amount of money that you want to bring to the Roulette Table.\n" \
        "In the betting phase you first choose between 6 different types of bet, and then select the" \
        "amount of money you want to place. You can repeat this process as often as you want or till" \
        "you run out of money. Afer the betting phase the virtual croupier will spin the roulette" \
        "weel, to determine the winning number and color.\n" \

        # asking the player how much money he wants to set and check if it's more then zero - if not ask again
        while True:
            playersmoney = raw_input(introduction+"How much money do want to bet?")
            try:
                playersmoney = int(playersmoney)
                if playersmoney>0:
                    break
            except ValueError:
                print("Please enter a number greater than 0!")

        # save player object into the roulettetabel object
        self.playerOnTable = Player(playername,playersmoney)

        # starting the betting phase through method of the object
        self.betting_phase()
        self.rotate_roulette()
        self.payout_phase()
        self.nextround()

        # asking player if he wants to play again + check if input is valid
        while True:
            answer = raw_input("Do want to play another round? (y/n)").lower()
            if answer in ['no','n','nein']:
                self.stop_playing()
            elif answer not in ['yes','y','ja']:
                print('Not valid answer. Please give y/yes or n/no')




    # starting the betting phase: the player can choose the option and bet a specific amount of money
    def betting_phase(self):

        # the user can set up several bets (as much as he wants)
        while True:
            # choosing the option
            while True:
                betting_option = raw_input("Choose a option you want to bet on. (use the number between the parenthesis)\n" \
                "The numbers in [ ] represent the payout of each bet.\n"
                "   (1) 'Straight' or 'Single' a bet on a single number [35 to 1]\n" \
                "   (2) 'Manque' or 'Passe' a bet on the first 18 {1-18} or second 18 {19-36} numbers. [1 to 1]\n" \
                "   (3) Red or Black or 'Rouge ou Noir' a bet on which color the roulette wheel will show. [1 to 1]\n" \
                "   (4) Even or odd 'Pair ou Impair' a bet on even or odd nonzero number. [1 to 1]\n" \
                "   (5) Dozen Bets a bet on the first 12 {1-12}, second 12 {13-24} or third 12 {25-36} numbers. [2 to 1]\n" \
                "   (6) Column Bets a bet on one of the three vertical lines e.g.: 1-4-7-10 . . . [2 to 1]\n" \
                "   (7) stop playing\n")

                try:
                    betting_option = int(betting_option)
                    if betting_option < 1:
                        raise ValueError
                except ValueError:
                    print("\nThis is not a valid number! Please try it again.")
                    continue

                while True:
                    # if the user gives a invalid input then he gets an message and can try it again
                    try:

                        # ask player on which number or group of numbers he wants to bet
                        if betting_option==1:
                            # ask for the number betwen 0 and 36
                            value = int(raw_input("You are betting on a single number.\n" \
                                    "Choose a number between 0 and 36: "))
                            if value < 0 or value >36:
                                raise ValueError
                        elif betting_option==2:
                            value = int(raw_input('Your are betting on the first 18 or second 18 numbers:' \
                                  'Please decide on which set you want to bet (use the number between the parenthesis):\n'\
                                  '   (1) Manque - first 18 {1-18}\n' \
                                  '   (2) Passe - second 18 {19-26}'))
                            if value < 0 or value >2:
                                raise ValueError
                        elif betting_option==3:
                            value = raw_input("Your are betting on 'red' or 'black'" \
                                    "Please decide on which you want to bet (red/black): ").lower()
                            if not any(value in ['red','black']):
                                raise ValueError
                        elif betting_option==4:
                            value = raw_input("Your are betting on 'even' or 'odd'" \
                                    "Please decide on which you want to bet (even/odd): ").lower()
                            if not any(value in ['even','odd']):
                                raise ValueError
                        elif betting_option==5:
                            value = int(raw_input("You chose the Dozen bets option" \
                                    "Please decide on which set of 12 numbers you want to bet (use the number between the parenthesis):\n" \
                                    "   (1) first 12 {1-12}\n" \
                                    "   (2) second 12 {13-24}\n" \
                                    "   (3) third 12 {25-36}\n"))
                            if value <1 or value >3:
                                raise ValueError
                        elif betting_option==6:
                            value = int(raw_input("You chose the Column bets option" \
                                    "Please decide on which column you want to bet (use the number between the parenthesis):\n" \
                                    "   (1) first column {1,4,7,10,13,16,19,22,25,28,31,34}\n" \
                                    "   (2) second column {2,5,8,11,14,17,20,23,26,29,32,35}\n" \
                                    "   (3) third column {3,6,9,12,15,18,21,24,27,30,33,36}\n"))
                            if value <1 or value >3:
                                raise ValueError
                        elif betting_option==7:
                            self.stop_playing()
                        break
                    except ValueError:
                        "This is not a valid input! Please try again."



                while True:
                    try:
                        money = float(raw_input("How much money do want to place?: "))
                        if money <=0:
                            raise ValueError
                    except ValueError:
                        "This is not a valid number! Please enter a number greater than 0."
                        continue

                    # take money from player
                    status = self.playerOnTable.loses(money)
                    if status == True:
                        break
                    print('You have only {} Euro left. Please bet less money.'.format(self.playerOnTable.getmoneystatus()))


                # save the amount of money which is left on the table
                self.addmoney2table(money)

                # save/log the bets
                self.playerOnTable.bets(betting_option,value,money)

                # ask if user wants to bet on another option + check if input valid
                while True:
                    answer = raw_input("To you want to bet on another option? (y/n): ").lower()
                    if answer in ['no','n','nein']:
                        return
                    elif answer in ['yes','y','ja']:
                        break
                    else:
                        print('This is not valid answer. You have to answer either y/yes or n/no')

    def rotate_roulette(self):
        self.roulette_number=random.randint(0,36)
        print("Roulette stopped at number {} !".format(self.roulette_number))

    # get color of the Roulette number
    def getcolor(self):
        if any(self.roulette_number in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]):
            return 'Red'
        elif self.roulette_number == 0:
            return 'No color (Zero)'
        else:
            return 'Black'

    # check if Roulette number is even or odd
    def checkeven(self):
        if self.roulette_number % 2 > 0:
            return False
        elif self.roulette_number==0:
            return None
        else:
            return True

    # add money to the table
    def addmoney2table(self,money):
        self.moneyOnTable += money

    # take money from the table
    def takemoneyfromtable(self,money):
        self.moneyOnTable -= money

    # this phase goes through all wins and loses
    def payout_phase(self):
        won_money = 0
        mainoptions = self.playerOnTable.getbetoptions()
        for option_elem in mainoptions:
            if option_elem==1:
                option = self.roulette_number
            if option_elem==2:
                option = 1 if self.roulette_number < 18 else 2
            if option_elem==3:
                option = self.getcolor()
            if option_elem==4:
                option = self.checkeven()
            if option_elem==5:
                if self.roulette_number > 12:
                    if self.roulette_number > 24:
                        option = 3
                    else:
                        option = 2
                else:
                    option = 1
            if option_elem==6:
                if self.roulette_number in [1,4,7,10,13,16,19,22,25,28,31,34]:
                    option = 1
                elif self.roulette_number in [2,5,8,11,14,17,20,23,26,29,32,35]:
                    option = 2
                elif self.roulette_number in [3,6,9,12,15,18,21,24,27,30,33,36]:
                    option = 3

            money = self.playerOnTable.getbettedmoney(option_elem,option)

            if money != None:
                won_money += self.playerOnTable.wins(self.winning_quote(mainoptions)*money)
                self.takemoneyfromtable(money)

        self.playerOnTable.loses(self.moneyOnTable)
        print("You won {} Euro and lost {} Euro!\n You now have {} Euro in total.".format(won_money,self.moneyOnTable,self.playerOnTable.getmoneystatus()))


    # gives back the winning quote for a specific bet-option
    def winning_quote(self,option):
        return [36,2,2,2,2,3,3][option-1]

    # delete saved number and color of the number  (not really necessary but 'cleaner'/more similar to Roulette)
    def nextround(self):
        self.roulette_number = None
        self.moneyOnTable = 0
        os.system('cls' if os.name == 'nt' else 'clear')

    # stops the program and gives the status of players money
    def stop_playing(self):
        print('You are leaving the Roulette table with {} Euro.'.format(self.playerOnTable.getmoneystatus()))
        exit()
