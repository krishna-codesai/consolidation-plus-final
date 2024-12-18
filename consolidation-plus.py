# imports the random module 
import random
import pandas as pd
import time

# Defined values and Target score to win the game
target = 50
max_re_rolls = 5

# Initializing the DataFrame for tracking rolls
roll_history_df = pd.DataFrame(columns=["Player", "Roll", "Turn"])

def roll_dice():
    """ Simulates rolling 3 dice. """
    return [random.randint(1, 6) for _ in range(3)]

def tuple_out(dice):
    """ Checks if all three dice are the same, indicating the player has 'tupled out'. """
    return dice[0] == dice[1] == dice[2]

def fixed_dice(dice):
    """ Identifies indices of dice that should be fixed if two dice are the same. """
    counts = {x: dice.count(x) for x in dice}
    fixed_indices = []
    # Defines what a fixed dice is 
    for i in range(len(dice)):
        if counts[dice[i]] == 2:
            fixed_indices.append(i)
    return fixed_indices


def re_roll_dice(dice, fixed_indices):
    """ Re-rolls only non-fixed dice """
    # Uses the fixed_indices from the fixed_dice function to identify what a fixed dice it 
    return[random.randint(1,6) if i not in fixed_indices else dice[i] for i in range(3)]

def get_player_choice(player_name):
    """ Validates the input for stopping or continuing the turn."""
    # Gives the user a chance to input "y" or "n" if the input is not valid the first time
    while True:
        # Makes sure that the user only uses "y" and "n" when asked if they want to continue
        #.strip() and .lower() make it so that white space and upper case doesn't matter
        choice = input(f"{player_name}, stop and keep score? (y/n): ").strip().lower()
        if choice in {"y", "n"}:
            return choice 
        else: 
            # Error message if input is invalid 
            print("Invalid input. Please enter 'y' or 'n'.")

def play_turn(player_name, computer=False):
    """ Plays one turn for a player."""
    dice = roll_dice()
    roll_history = [tuple(dice)]
    print(f"{player_name} rolls: {dice}")
    
    # Check if the player tupled out
    if tuple_out(dice):
        print(f"Tuple out! {player_name} scores 0 points this turn.")
        return 0

    # Check if the player rolled a fixed dice 
    fixed = fixed_dice(dice)
    if fixed:
        print(f"{player_name} rolled a fixed dice! The score will be kept.")
        score = sum(dice)
        print(f"{player_name} scores {score} points this turn.")
        print(f"Roll history for this turn: {roll_history}")
        return score

    re_roll_count = 0  # Initialize re-roll count

    while re_roll_count < max_re_rolls:  
        # Limit the number of rerolls
        if computer:
            stop = "y" if sum(dice) >= 12 or random.choice([True, False]) else "n"
        else:
            stop = get_player_choice(player_name)

        # If the player decides to stop the game 
        if stop == "y":
            score = sum(dice)
            print(f"{player_name} scores {score} points this turn.")
            print(f"Roll history for this turn: {roll_history}")
            return score

        # If the player decides to re-roll
        re_roll_count += 1
        # Re-roll only non-fixed dice 
        dice = re_roll_dice(dice, fixed) 
        roll_history.append(tuple(dice))
        print(f"{player_name} re-rolls: {dice}")

        # Check for tuple out after re-roll
        if tuple_out(dice):
            print(f"Tuple out! {player_name} scores 0 points this turn.")
            return 0

        # Recalculate fixed dice after each re-roll
        fixed = fixed_dice(dice) 
        if fixed:
            print(f"{player_name} rolled fixed dice: {dice}. Turn ends.")
            score = sum(dice)
            print(f"{player_name} scores {score} points this turn.")
            print(f"Roll history for this turn: {roll_history}")
            return score



# Initializes scores
scores = [0, 0]
# Defines player names 
player_names = ["Player 1", "Player 2"]
# Initializes current_player variable 
current_player = 0

# Game loop 
# While the max scores are less than the target score
while max(scores) < target:
    # Message that tells player's whose turn it is  
    print(f"\n{player_names[current_player]}'s turn!")
    # Score that the player earns each turn 
    turn_score = play_turn(player_names[current_player])
    scores[current_player] += turn_score
    print(f"{player_names[current_player]}'s total score: {scores[current_player]}")
    # Swtiches players 
    current_player = 1 - current_player  
# How the winner is determined 
winner = player_names[0] if scores[0] >= target else player_names[1]
# Winner message 
print(f"\n{winner} wins with a score of {max(scores)}!")
