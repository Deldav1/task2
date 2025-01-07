import random
import time

# Function to only load 5-letter words from a file into a list
def load_words(filename):
    try:
        # Check if the file exists and can be opened
        print(f"Opening file: {filename}")  
        with open(filename, "r") as file:
            words = file.read().splitlines()
            return [word.lower() for word in words if len(word) == 5]

    # Error handling 
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Filepath to the dictionary.txt file
word_list = load_words(r"C:\Users\spiri\Desktop\task2\dictionary.txt")  

if word_list:
    print(f"Loaded {len(word_list)} 5-letter words.")
else:
    print("No valid words loaded.")



# Uses the random function to select a word
def select_random_word(word_list):
    if word_list:
        return random.choice(word_list)
    else:
        print("The word list is empty.")
        return None 



# Function to get a guess from the user and error check it
def get_guess():
    start_time = time.time() 
    guess = input("A word has been chosen, What is your guess? ").lower()

    while len(guess) != 5 or not guess.isalpha():  
        elapsed_time = time.time() - start_time
        if elapsed_time > 30:
            print(f"You took longer than 30s. This guess is invalid.")
            return None
        print("Your input was invalid, please enter a 5 letter word.")
        guess = input("Enter your 5 letter guess: ").lower()

    # Check if time exceeded after loop finishes
    elapsed_time = time.time() - start_time
    if elapsed_time > 30:
        print(f"You took too long to guess, this guess is invalid.")
        return None

    return guess



# Makes sure the guess is actually part of the set dictionary of words
def is_valid_guess(guess, word_list):
    return guess in word_list
    


# This checks for correct letters in the correct place
def provide_clue(guess, chosen_word):
    clue = []
    chosen_word_list = list(chosen_word)

    for i in range(5):
        if guess[i] == chosen_word[i]:
            clue.append("*")
            chosen_word_list[i] = None
        else:
            clue.append(None)

    for i in range(5):
        if clue[i] is None and guess[i] in chosen_word_list:
            clue[i] = ("+")
            chosen_word_list[chosen_word_list.index(guess[i])] = None  # Removes letter from consideration

    for i in range(5):
        if clue[i] is None:
            clue[i] = "_"

    return "".join(clue)


# Handles turn on whether the guess was correct 
def handle_turn(guess, chosen_word, word_list, invalid_guesses):
    if guess == chosen_word:
        return "Congratulations you have guessed the word!", invalid_guesses
    else:
        clue = provide_clue(guess, chosen_word)

        for char in guess:
            if char not in chosen_word and char not in invalid_guesses:  # Checks if character is in the chosen word and the invalid guesses list, if both return false then adds the character to the list
                invalid_guesses.append(char)
        return clue, invalid_guesses



def display_result(is_winner, attempts, chosen_word):
    if is_winner:
        print(f"Congrats. You have guessed the word '{chosen_word}' in {attempts} attempts.")
    else:
        print(f"You have lost. The chosen word was '{chosen_word}'.")



def give_up(chosen_word):
    print(f"You have given up. The chosen word was  '{chosen_word}'.")



def record_player_name():
    name = input("Please enter your name: ")
    return name



def the_winner(time_taken, name):
    try:
        print(f"time taken type: {type(time_taken)}")
        with open("winners.txt", "a") as file:
            file.write(f"{name} completed the game in {float(time_taken):.2f} seconds.\n")
    except Exception as e:
        print(f"Error whilst recording the winner: {e}")



def main_game():
    player_name = record_player_name()
    start_time = time.time()
    chosen_word = select_random_word(word_list)
    guesses_taken = 0
    max_guesses = 6
    print(f"the chosen word is: {chosen_word}")

    print(f"Welcome {player_name}. Lets play wordle.")

    while guesses_taken < max_guesses:
        print(f"Attempt {guesses_taken + 1} of {max_guesses}:")

        guess = get_guess()

        if guess is None:
            continue

        if guess == chosen_word:
            elapsed_time = float(time.time() - start_time)
            print(f"Congrats {player_name}, You guessed the word {chosen_word} in {elapsed_time:.2f} seconds.")
            the_winner(player_name, elapsed_time)
            return

        clue = provide_clue(guess, chosen_word)
        print(f"Clue: {clue}")

        guesses_taken += 1

    elapsed_time = float(time.time() - start_time)
    print(f"You have used up all of your guesses. The word was '{chosen_word}'.")
    print(f"Game over, you took '{elapsed_time}' seconds.")
    the_winner(record_player_name, elapsed_time)
    
   

if __name__ == "__main__":
    main_game()