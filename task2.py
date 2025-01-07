import random
import time

# Function to only load 5-letter words from a file into a list
def load_words(filename):
    try:
        # Check if the file exists and can be opened  
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

# Function to make sure the guess is actually part of the dictionary
def is_valid_guess(guess, word_list):
    return guess in word_list

# Function to get a guess from the user and error check it
def get_guess(word_list):  # Pass word_list to the function
    start_time = time.time()
    guess = input("What is your guess? ").lower()

    # Loop to ensure the guess is 5 letters long and a valid word in the dictionary
    while len(guess) != 5 or not is_valid_guess(guess, word_list):  
        elapsed_time = time.time() - start_time
        if elapsed_time > 30:
            print(f"You took too long. This guess is invalid.")
            return None
        print("Your input was invalid. Please enter a 5-letter word that exists in the dictionary.")
        guess = input("Enter your 5-letter guess: ").lower()

    return guess

# Function to select a random word from the word list
def select_random_word(word_list):
    if word_list:
        return random.choice(word_list)
    else:
        print("The word list is empty.")
        return None 

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
            clue[i] = "+"
            chosen_word_list[chosen_word_list.index(guess[i])] = None  # Removes letter from consideration

    for i in range(5):
        if clue[i] is None:
            clue[i] = "_"

    return "".join(clue)

# Function to record player name
def record_player_name():          
    name = input("Please enter your name: ")
    return name.capitalize()

# Function to add player data to winners.txt file if they win
def the_winner(name, time_taken, chosen_word):   
    try:
        with open("winners.txt", "a") as file:
            chosen_word_upper = chosen_word.upper()
            file.write(f"{name} completed the game successfully and guessed the word {chosen_word_upper} in {float(time_taken):.2f} seconds.\n") 
    except Exception as e:
        print(f"Error whilst recording the winner: {e}")

# Main game function
def main_game():         
    word_list = load_words(r"C:\Users\spiri\Desktop\task2\dictionary.txt")  # Loading word list here
    if not word_list:
        print("No valid words loaded. Exiting game.")
        return

    player_name = record_player_name()
    start_time = time.time()
    chosen_word = select_random_word(word_list)
    guesses_taken = 0
    max_guesses = 6

    print(f"Welcome {player_name}. Let's play Wordle!")

    while guesses_taken < max_guesses:
        print(f"Attempt {guesses_taken + 1} of {max_guesses}:")           

        guess = get_guess(word_list)  # Pass word_list here to validate guesses

        # Always increment attempts here
        guesses_taken += 1

        if guess is None:
            print("Your guess was invalid or took too long. Skipping turn.")
            continue  # Skip the turn if the guess is invalid or took too long

        # If the guess is correct, the game ends
        if guess == chosen_word:
            elapsed_time = float(time.time() - start_time)     # Checking if the player's word matches the chosen word, records the time taken and calls the_winner function
            chosen_word_upper = chosen_word.upper()            
            print(f"Congrats {player_name}, You guessed the word {chosen_word_upper} in {elapsed_time:.2f} seconds.")
            the_winner(player_name, elapsed_time, chosen_word)  # Only call the_winner if the player wins
            return

        # If guess is incorrect, give clue and continue to next turn
        clue = provide_clue(guess, chosen_word)
        print(f"Clue: {clue}")
    
    # If the player loses, no winner is recorded.
    elapsed_time = float(time.time() - start_time)
    print(f"You have used up all of your guesses. The word was '{chosen_word}'.")    
    print(f"Game over, you took {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main_game()
