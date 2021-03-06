# Class creates the hangman game once instantiated.
# Users are given 5 attempts to guess a random word

import os  # operating system module used to easily interact with the file structure
from random import choice  # random module used to generate a random entry from a list of words. From is used as we
# only need the choice function from the random module. We can also now refer to the choice function as .choice() not
# random.choice(), allowing code to be more concise
import config  # config module gives access to global styling


class Hangman:
    """ Class creates the hangman game. User is given 8 attempts to guess a random 5 letter word """

    def __init__(self):
        # variable contains program on or off state, always start as True to indicate menu running
        self.is_running = True
        self.replay = True  # variable used to control if user is asked if they want to retry the game

        self.word_list = []  # holds imported word list from word_list.txt.txt
        self.word = ""  # string holds the current word for the user to guess

        self.word_letters = []  # list holds each of the random words letters
        self.guessed_word = ""  # string holds the users correct guesses
        self.guessed_letters = []  # list holds all guessed letters
        self.guess_counter = 8  # variable holds the amount of guesses a user has left

        print("🆆🅴🅻🅲🅾🅼🅴 🆃🅾 🆃🅷🅴 🅷🅰🅽🅶🅼🅰🅽 🅶🅰🅼🅴".center(45))  # give user starting instructions
        print('\nTo return to the main menu just type "exit" at any time')
        print('To get help just type "help" at any time')

        self.word_import()  # import the word list form word_list.txt.txt
        self.hangman_start()  # trigger the hangman_start method to provide user instructions

    # method imports the word_list.txt.txt data into the feature module
    def word_import(self):
        # os.path.join allows the given file path to work on windows, linux and mac systems
        # Windows systems use '\' between directories, but linux and mac use '/'. os.path.join automatically
        # works this out based on the users operating system, generating the correct file path
        file = os.path.join("data", "word_list.txt")
        # word_list.txt is the file we want to read from the data directory

        with open(file, "r") as file:
            for line in file:
                # loop through each line in the file, and add it to the list.
                self.word_list.append(line.strip())

        self.word = choice(self.word_list)  # once list is built, add a random entry to the self.word variable
        self.word_letters = list(self.word)  # break the word down into a list of letters

    # method guides the user through the game, looping each time the user enters an input until the game ends
    def hangman_start(self):
        """ method starts the hangman game, requesting user inputs to check against letters in a random word """
        while self.is_running:  # when this while loop breaks, we return to the main module
            self.word_mask()  # masks the characters in the word which the user hasn't guessed yet
            print("\n-------------------------------------------------------\n")  # line divides guesses
            print("The word you are guessing is {}".format(self.guessed_word))
            print("You have {} guesses left".format(self.guess_counter))
            if len(self.guessed_letters) > 0:  # check to see if list has entries. If it doesnt dont show message
                print("You have already guessed these letters: {}".format(self.guessed_letters))

            # while word is masked - loop the following actions!
            letter_guess = self.input_check()
            if letter_guess == "exit":  # check for the "exit" keyword.
                print("Goodbye from the hangman game! \U0000263B")
                self.replay = False  # ensure user doesnt get asked to replay quiz at the end
                break  # if "exit" found we break the loop, leaving this feature module
            self.guessed_letter_check(letter_guess)  # method checks if the letter is in the self.word variable
            self.guessed_letters.append(letter_guess)  # add the guessed letter to the guessed letter list
            self.word_mask()  # reveal correctly guessed letters in the guessed_word variable, everything else is a '*'
            self.completed_check()  # method checks to see if word has been guessed correctly or all turns used
        self.replay_check()  # ask user if they want to play again- if yes game state is reset, if no, game exits

    # method used to hide the word, making all unknown characters * symbols
    def word_mask(self):
        """ Method checks the users input letters, revealing them on the word to find if they match """
        self.guessed_word = ""  # set the word to an empty string
        for entry in self.word_letters:  # loop through each character in the word_letter array (5)
            if entry in self.guessed_letters:  # loop though all of the letters a user has guessed
                # If a letter matches, the letter is concatenated to the guessed_word variable
                self.guessed_word += entry
            else:
                # If a letter isn't found, a * is concatenated to the guessed_word variable
                self.guessed_word += "*"

    # method checks to ensure correct string is entered by user
    def input_check(self):
        """ Method handles the user input ensuring its valid whilst looking for keywords 'exit' and 'help' """
        user_input = ""  # ensure user_input is cleared
        while self.is_running:  # while loop ensures user gives a valid input
            user_input = input(": ")
            if len(user_input) > 1:  # check to see if user_input length is greater than 1 character
                if user_input.lower() == "exit":
                    self.is_running = False  # statement breaks input while loops
                    user_input = user_input.lower()  # .lower ensures the input is returned in correct format
                elif user_input.lower() == "help":  # if/else statement controls tailored help messages
                    print("\nYou are in the hangman game! Type in a single letter to guess the word")
                else:  # user didnt enter "help" or "exit" but put in more than one letter
                    print("\nYou can only input a single letter, please try again 👍")
            else:
                break  # input is a valid single character, break the loop to return the user input
        return user_input  # return the valid input

    # method checks to see if users guess is in the random word, if not decreases the guess_counter
    def guessed_letter_check(self, user_input):
        """ Method checks user input argument to see if its a valid character in the word they are guessing.
        If not the counter decreases """
        if user_input not in self.word:
            self.guess_counter -= 1  # decrease the counter by 1. Game ends at 0 after 5 guesses

    # method checks to see if a user has won or lost the game, breaking the is_running while loop either way
    def completed_check(self):
        """ Method checks to see if the users created word, made up of guesses, matches the random word """
        if self.word == self.guessed_word:
            print(config.Style.bold, "\n*** Congratulations you successfully guessed the word! ***",
                  config.Style.end, config.Style.purple)  # winning message in bold
            self.is_running = False  # setting variable to false breaks the play loop
        elif self.guess_counter == 0:  # if guessed more than 8 times player loses and game ends
            print(config.Style.bold, "\n*** You didn't manage to guess the word this time! ***",
                  config.Style.end, config.Style.purple)  # losing messaged in bold
            print("The word was {}".format(self.word))
            self.is_running = False  # variable breaks the input loops

    # method checks to see if user wants to replay the game after its finished
    def replay_check(self):
        """ Method asks user if they would like to replay the game """
        while self.replay:
            print("\nWould you like to play again?")
            replay = input("Enter '1' for yes, '2' for no: ")
            if replay == "1":
                # if user wants to restart we need to reset game state and restart
                self.word = choice(self.word_list)  # get a new random word from list of possible words
                self.word_letters = list(self.word)  # list holds a list of all the random words letters
                self.guessed_word = ""  # string holds the users correct guesses
                self.guessed_letters = []  # list holds all guessed letters
                self.guess_counter = 8  # re-set try counter to 5
                self.is_running = True  # re-enter the start loop
                self.hangman_start()  # restart the game
            elif replay == "2" or replay.lower() == "exit":  # user wants to leave the game
                print("Goodbye from the hangman game! \U0000263B")
                self.replay = False
                # leaving the method will cause the script to end and put the user back to the main menu
            elif replay.lower() == "help":
                print("\nYou are in the hangman game! Type in '1' to play again, or '2' to exit the game")
