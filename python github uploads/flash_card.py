import csv
import random
import time
import sys

DELAY = 0.05
TRIAL = 10


def read_from_csv():
    abbreviations = "abbreviations.csv"
    # Read data from csv file
    with open(abbreviations, "r") as external_connection:
        iterable_object_pointer = csv.DictReader(external_connection)
        abbr_dict = list(iterable_object_pointer)
    return abbr_dict
        

def format_data_structure(nested_data_structure):
    # Split the nested data structure into 3 lists of dictionaries
    categorized_cards = {
        "easy": [],
        "medium": [],
        "hard": []
    }

    for card in nested_data_structure:
        difficulty = card['difficulty'].strip().lower()
        if difficulty in categorized_cards:
            # Dynamically target the sub-list using the difficulty string as a key!
            categorized_cards[difficulty].append(card)
            
    return categorized_cards

def start_game(categorized_cards):
    level = validate_input()
    result = display_cards(level, categorized_cards)
    print_characters(f"You scored {result} out of {TRIAL}.\n")
    if result > 7:
        print_characters("You did wonderful. You have a good mastery of the terminologies.")
    elif result <= 6:
        print_characters("Great trial! You can do better next time.\nRemember! Practice beats talent!\n")

def validate_input():
    while True:
        print_characters("Which level would you like to try? ")
        user_input = input(" ")
        input_checker = user_input.strip().lower()

        if input_checker == 'easy':
            return input_checker
        elif input_checker == 'medium':
            return input_checker
        elif input_checker == 'hard':
            return input_checker
        else:
            print_characters(f"'{input_checker}' is an invalid input. Enter 'easy' or 'medium' or 'hard'\n")

def print_characters(text):
    # Split the sentence into a list of individual words
    
    for character in text:
        # Print the word followed by a space, keeping the cursor on the same line
        sys.stdout.write(character)
        # Force the console to display the text right now instead of buffering it
        sys.stdout.flush()
        # Pause for a fraction of a second before the next word
        time.sleep(DELAY)


def display_info():
    print("---------------The Flashcard game------------------")
    print_characters("\nWould you like to test your knowledge on common computer science abbreviations? Press ENTER to continue.")
    # Validation: 
    # If the user presses ENTER, they are ready to play. Otherwise, ask them if they really want to exit the game
    exit_code = -1
    while not (exit_code == 1):
        user_press = input(" ")
        # Condition A: User wants to play
        if len(user_press.strip()) == 0:
            break
        # Condition B: User wants to exit
        elif user_press.strip().lower() == 'exit':
            if exit_code == -1:
                print_characters("\nDo you really want to exit the game?")
                print_characters("\nPress ENTER to play. Type 'exit' to end the game: ")
                exit_code += 1
            # Because the user typed 'exit' a second time, we don't want to show them the warning again.
            elif exit_code == 0:
                exit_code += 1
        # Condition C: User types a random character
        else:
            print_characters("\nPress ENTER to play or type 'exit' to stop playing: ")
    
    if exit_code == 1:
        # terminate the game.
        print_characters("\nThank you for visiting! Goodbye!\n")
        return True # signal to caller function to terminate the game

    print_characters("\nThere are 3 levels of complexities to this game: Easy, Medium and Hard levels.\n")
    print_characters("A card of the chosen complexity will pop up with an abbreviated terminology.\n")
    print()
    print_characters("All you need to do is provide its full name.\n")

    return False # signal to continue with the game


def display_cards(complexity, all_cards):
    chosen_cards = all_cards[complexity]
    # Defensive check: Make sure we don't sample more cards than exist in that category
    actual_trials = min(TRIAL, len(chosen_cards))
    print_characters(f"You are going to attempt {actual_trials} abbreviations.\n")
    print()
    
    correct_responses = 0
    deck_of_cards = random.sample(chosen_cards, TRIAL)
    for random_card in deck_of_cards:
        print_characters(f"What is the full name of {random_card['abbreviation']}? ")
        user_input = input(" ")
        check = match_full_name(user_input, random_card)

        if check:
            print_characters("Correct!\n")
            correct_responses += 1
        else:
            print_characters(f"Good trial! The full name of {random_card['abbreviation']} is {random_card['full_name']}.\n")        
        print()
    return correct_responses

def match_full_name(answer, card):
    # Grab the correct answer, lowercase it, and remove trailing whitespace. Also convert hyphens into standard spaces
    # Treat both 'object-oriented' and 'object oriented' similarly
    correct_answer = card['full_name'].strip().lower().replace("-", " ")
    
    # Lowercase and clean the raw user's input. Also convert hyphens to spaces
    user_answer = answer.strip().lower().replace("-", " ")
    # Replace double spaces with single spaces catching accidental double-tapping of the spacebar
    correct_cleaned_answer = " ".join(correct_answer.split())
    user_cleaned_answer = " ".join(user_answer.split())

    return user_cleaned_answer == correct_cleaned_answer # Returns either True or False

def main():
    # Load and format the data once at the very start
    abbreviations = read_from_csv()
    categorized_cards = format_data_structure(abbreviations)

    # The function returns a signal on whether to stop the game or not.
    should_terminate_game = display_info()
    if should_terminate_game:
        return

    # Start the continuous game loop
    exit_game_loop = False
    while not exit_game_loop:
        start_game(categorized_cards)
        # Ask the user if the want to keep playing
        print_characters("\nWould you like to play another round? (yes/no): ")

        # Enter the input validation loop.
        while True:
            choice = input(" ").strip().lower()
            # Using a list of all possible choices, validate user choice
            # If user enters a valid choice, exit the validation loop and possibly the game loop.
            if choice in ['yes', 'y', 'no', 'n']:
                # Exit the validation loop but remain in the game loop.
                if choice == 'yes' or choice == 'y':
                    print_characters("\nGreat! Let's try another round.\n")
                    break # The validation loop exit
                # Exit both the validation and game loops.
                else:
                    print_characters("\nThank you for playing! Keep practicing and see you next time!\n")
                    exit_game_loop = True
                    break
            # Remain in the validation loop until user enters a correct choice.
            else:
                print_characters("\nInvalid choice! Select either (yes/y) or (no/n): ")



if __name__ == '__main__':
    main()