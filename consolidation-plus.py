# imports the random module 
import random
import pandas as pd
import time

# Defined values and Target score to win the game
target = 50
max_re_rolls = 5

# Initializing the DataFrame for tracking rolls
roll_history_df = pd.DataFrame(columns=["Player", "Roll", "Turn"])

#Initializes the three dice ranging from 1-6
def roll_dice():
    """ Simulates rolling 3 dice. """
    return [random.randint(1, 6) for _ in range(3)]

#Initializes the tuple out feature if three of the numbers are all the same
def tuple_out(dice):
    """ Checks if all three dice are the same, indicating the player has 'tupled out'. """
    return dice[0] == dice[1] == dice[2]

#Fixed dice feature moves onto second player if two numbers are the same
def fixed_dice(dice):
    """ Identifies indices of dice that should be fixed if two dice are the same. """
    counts = {x: dice.count(x) for x in dice}
    fixed_indices = []
    for i in range(len(dice)):
        if counts[dice[i]] == 2:
            fixed_indices.append(i)
    return fixed_indices

#Initializes the ability to reroll the dice
def re_roll_dice(dice, fixed_indices):
    """ Re-rolls only non-fixed dice """
    return [random.randint(1, 6) if i not in fixed_indices else dice[i] for i in range(3)]


#Initializes the yes and no options for the players
def get_player_choice(player_name):
    """ Validates the input for stopping or continuing the turn. """
    while True:
#Two character options for the player to choose from
        choice = input(f"{player_name}, do you want to stop and keep your score? (y/n): ").strip().lower()
        if choice in {"y", "n"}:
            return choice 
        else: 
#Makes sure that there is an error message and points out an error if anything besides y or n is selected
            print("Invalid input. Please enter 'y' or 'n'.")

#Initializes the player turns
def play_turn(player_name):
    """ Plays one turn for a player. """
    global roll_history_df
    dice = roll_dice()
    roll_history = [tuple(dice)]
    print(f"{player_name} is rolling the dice...")
    time.sleep(1)  # Add suspense
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
        roll_history_df = pd.concat([
            roll_history_df,
            pd.DataFrame([{"Player": player_name, "Roll": dice, "Turn": 0}])
        ], ignore_index=True)
        return score

    re_roll_count = 0  # Initialize re-roll count

    while re_roll_count < max_re_rolls:
        stop = get_player_choice(player_name)  # Call get_player_choice here
        if stop == "y":
            score = sum(dice)
            print(f"{player_name} scores {score} points this turn.")
            print(f"Roll history for this turn: {roll_history}")
            roll_history_df = pd.concat([
                roll_history_df,
                pd.DataFrame([{"Player": player_name, "Roll": dice, "Turn": re_roll_count}])
            ], ignore_index=True)
            return score

        re_roll_count += 1
        dice = re_roll_dice(dice, fixed)
        roll_history.append(tuple(dice))
        print(f"{player_name} re-rolls: {dice}")

        if tuple_out(dice):
            print(f"Tuple out! {player_name} scores 0 points this turn.")
            roll_history_df = pd.concat([
                roll_history_df,
                pd.DataFrame([{"Player": player_name, "Roll": dice, "Turn": re_roll_count}])
            ], ignore_index=True)
            return 0

        fixed = fixed_dice(dice)
        if fixed:
            print(f"{player_name} rolled fixed dice: {dice}. Turn ends.")
            score = sum(dice)
            print(f"{player_name} scores {score} points this turn.")
            print(f"Roll history for this turn: {roll_history}")
            roll_history_df = pd.concat([
                roll_history_df,
                pd.DataFrame([{"Player": player_name, "Roll": dice, "Turn": re_roll_count}])
            ], ignore_index=True)
            return score

    return 0  # Ensure a return value if no conditions are met

# Initializes scores
scores = [0, 0]
player_names = ["Player 1", "Player 2"]
current_player = 0

# Game loop
while max(scores) < target:
    print(f"\n{player_names[current_player]}'s turn!")
    start_time = time.process_time()
    turn_score = play_turn(player_names[current_player])
    end_time = time.process_time()
    print(f"Turn processing time for {player_names[current_player]}: {end_time - start_time:.2f} seconds")
    scores[current_player] += turn_score
    print(f"{player_names[current_player]}'s total score: {scores[current_player]}")
    current_player = 1 - current_player

#Addresses the winner and scores of the players
winner = player_names[0] if scores[0] >= target else player_names[1]
print(f"\n{winner} wins with a score of {max(scores)}!")

# Analyze roll history and provides the statistics of each time and player
print("\nGame Statistics:")
for player in player_names:
    player_data = roll_history_df[roll_history_df["Player"] == player]
    print(f"{player}:")
    print(f" - Total Rolls: {len(player_data)}")
    if not player_data.empty:
        print(f" - Average Score: {player_data['Roll'].apply(sum).mean():.2f}")
        print(f" - Most Frequent Value: {pd.Series([val for sublist in player_data['Roll'] for val in sublist]).mode()[0]}")
