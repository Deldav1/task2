import random
import time

# function to only load 5 letter words from dictionary file
def load_words(filename):
    try:
        # checks that file exists and can be opened
        with open(filename, "r") as file:
            words = file.read().splitlines()
            return [word.lower() for word in words if len(word) == 5]
        # error handling
    except FileNotFoundError:                                           
        print(f"Error: The file '{filename}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    # function makes sure guess is in the dictionary file and valid
def is_valid_guess(guess, word_list):
    return guess in word_list

# gets a guess from the player and error checks it
def get_guess(word_list):  
    start_time = time.time()
    guess = input("What is your guess? ").lower()

    if guess == "give up":      # handles the give up function
        print()
        return "give up"

    elapsed_time = time.time() - start_time
    if elapsed_time > 30:                                         # makes guess invalid if time taken is longer than 30s
        print(f"You took too long. This guess is invalid.")
        return None
        print("Your input was invalid. Please enter a 5-letter word that exists in the dictionary.")
        guess = input("Enter your 5-letter guess: ").lower()

    if len(guess) != 5 or not is_valid_guess(guess, word_list):      # if guess is incorrect, returns None and skips attempt
        return None 
       

    return guess

# selects random word from the list made from dictionary
def select_random_word(word_list):
    if word_list:
        return random.choice(word_list)
    else:
        print("The word list is empty.")
        return None 

    # checks for the characters given by the player being in the chosen word
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
            chosen_word_list[chosen_word_list.index(guess[i])] = None  # removes letter from consideration

    for i in range(5):
        if clue[i] is None:
            clue[i] = "_"

    return " ".join(clue)

# function records the player's name
def record_player_name():          
    name = input("Please enter your name: ")
    print()
    return name.capitalize()

# function to add the player data to a winner.txt file if they win
def the_winner(name, time_taken, chosen_word):   
    try:
        with open("winners.txt", "a") as file:
            chosen_word_upper = chosen_word.upper()
            file.write(f"{name} completed the game successfully and guessed the word {chosen_word_upper} in {float(time_taken):.2f} seconds.\n") 
    except Exception as e:
        print(f"Error whilst recording the winner: {e}")

        # main game function
def main_game():         
    word_list = load_words(r"C:\Users\spiri\Desktop\task2\dictionary.txt")  # loads word_list
    if not word_list:
        print("No valid words loaded. Exiting game.")
        return
    
    player_name = record_player_name()
    start_time = time.time()
    chosen_word = select_random_word(word_list)
    guesses_taken = 0
    max_guesses = 6
    incorrect_guesses = []

    print(f"If you chose to give up type 'give up' at any time to end the game and reveal the word")    # give up notice
    print(f"Welcome {player_name}. Let's play Wordle!")
    print()
    print(f"The following symbols mean : \n * - The character is in the word and in the correct place. \n + - The character is in the word but in the incorrect place. \n _ - The chracter is not in the chosen word.")
    print()

    while guesses_taken < max_guesses:
        print(f"Attempt {guesses_taken + 1} of {max_guesses}:")          
        print(f"Incorrect guesses: {', '.join(incorrect_guesses)}")

        guess = get_guess(word_list)  # validates guesses

        guesses_taken += 1

        if guess == "give up":
            print(f"You gave up. The word was '{chosen_word}'.")
            print(f"Hope you play again soon, {player_name}.")
            return

        if guess is None:
            print("Your guess was invalid or took too long. Skipping turn.")
            print()
            continue  

        if guess == chosen_word:
            elapsed_time = float(time.time() - start_time)     # Checking if the player's word matches the chosen word, records the time taken and calls the_winner function
            chosen_word_upper = chosen_word.upper()            
            print(f"Congrats {player_name}, You guessed the word {chosen_word_upper} in {elapsed_time:.2f} seconds.")
            the_winner(player_name, elapsed_time, chosen_word)  # Only call the_winner if the player wins
            return

        # If guess is incorrect, give clue and continue to next turn
        clue = provide_clue(guess, chosen_word)
        print(f"Clue: {clue}")
        print()

        for letter in guess:
            if letter not in chosen_word and letter not in incorrect_guesses:
                incorrect_guesses.append(letter)
    
    # If the player loses, no winner is recorded.
    elapsed_time = float(time.time() - start_time)
    print(f"You have used up all of your guesses. The word was '{chosen_word}'.")    
    print(f"Game over, you took {elapsed_time:.2f} seconds.")
    print()

if __name__ == "__main__":
    main_game()            # ensures that code is executed directly, avoids unintended issues
