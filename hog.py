"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    total = 0
    rolled_one = False
    for n in range(num_rolls):
        outcome = dice()
        if outcome == 1:
            rolled_one = True
        total += outcome
    
    if rolled_one:
        total = 1
    
    return total
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    opponent_ones = score % 10
    opponent_tens = (score // 10) % 10
    return 10 - opponent_ones + opponent_tens
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        points_scored = free_bacon(opponent_score)
    else:
        points_scored = roll_dice(num_rolls, dice)
    return points_scored
    # END PROBLEM 3


def is_swap(player_score, opponent_score):
    """
    Return whether the two scores should be swapped
    """
    # BEGIN PROBLEM 4
    player_score_ones = player_score % 10
    opponent_score_ones = opponent_score % 10
    opponent_score_tens = (opponent_score // 10) % 10 # Works for triple digits

    difference = abs(player_score_ones - opponent_score_ones)
    
    swap = False
    if difference == opponent_score_tens:
        swap = True
    return swap    
    # END PROBLEM 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence, feral_hogs=True):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    feral_hogs: A boolean indicating whether the feral hogs rule should be active.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    player0_prev_turn_points, player1_prev_turn_points = 0, 0
    player0_commentary = say
    while max(score0, score1) < goal: 
        # PLAYER0's turn
        player0_num_rolls = strategy0(score0, score1)
        player0_turn_points = take_turn(player0_num_rolls, score1, dice)
        score0 += player0_turn_points

        # PLAYER0_NUM_ROLLS is 2 away from points scored on previous turn
        if feral_hogs:
            extra = is_extra(player0_num_rolls, player0_prev_turn_points)
            if extra:
                score0 += 3

        # SCORE0 and SCORE1 ones digits difference equals SCORE1 tens digit 
        swap = is_swap(score0, score1) 
        if swap:
            score0, score1 = score1, score0
        player0_prev_turn_points = player0_turn_points
        
        # PLAYER0's commentary (return value is PLAYER1's commentary)
        player1_commentary = player0_commentary(score0, score1)

        # PLAYER1's turn (only taken if goal has not been reached)
        if max(score0, score1) < goal:
            player1_num_rolls = strategy1(score1, score0)
            player1_turn_points = take_turn(player1_num_rolls, score0, dice)
            score1 += player1_turn_points
            
            # PLAYER1_NUM_ROLLS is 2 away from points scored on previous turn
            if feral_hogs:
                extra = is_extra(player1_num_rolls, player1_prev_turn_points)
                if extra:
                    score1 += 3
            
            # SCORE0 and SCORE1 ones digits difference equals SCORE1 tens digit 
            swap = is_swap(score1, score0)
            if swap:
                score1, score0 = score0, score1
            player1_prev_turn_points = player1_turn_points 
        
            # PLAYER1's commentary (return value is PLAYER0's commentary)
            player0_commentary = player1_commentary(score0, score1) 
    return score0, score1


def is_extra(num_rolls, prev_turn_points):
    if abs(num_rolls - prev_turn_points) == 2:
        return True
    return False


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 17)
    Player 0 now has 6 and Player 1 now has 17
    Player 1 takes the lead by 11
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 11)
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 11)
    >>> f4 = f3(13, 20)
    >>> f5 = f4(20, 35)
    15 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 47) # Player 1 gets 12 points; not enough for a new high
    >>> f7 = f6(21, 47)
    >>> f8 = f7(21, 77)
    30 point(s)! That's the biggest gain yet for Player 1
    >>> f9 = f8(77, 22) # Swap!
    >>> f10 = f9(33, 77) # Swap!
    55 point(s)! That's the biggest gain yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def say(score0, score1):
        if who == 0:
            score, score_opponent = score0, score1
        else:
            score, score_opponent = score1, score0
        
        turn_increase = score - last_score 
        if turn_increase > running_high:
            new_running_high = turn_increase
            print(new_running_high, 'point(s)! That\'s the biggest gain yet', 
                  'for Player', who)
            # RUNNING_HIGH has increased
            return announce_highest(who, score, new_running_high)
        # RUNNING_HIGH has not increased
        return announce_highest(who, score, running_high)
    return say
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def original_function_trials_times(*args):
        current_trial = 0
        total = 0.0
        while current_trial < trials_count:
            total += original_function(*args)
            current_trial += 1
        average = total / trials_count
        return average
    return original_function_trials_times
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    averaged_roll_dice = make_averaged(roll_dice, trials_count)

    num_rolls_averages = []
    for i in range(1, 11): # Number of dice from 1 to 10
        num_rolls_avg = averaged_roll_dice(i, dice) 
        num_rolls_averages.append(num_rolls_avg) 

    optimal_num_rolls = find_max_scoring_num_rolls(num_rolls_averages)
    return optimal_num_rolls
    # END PROBLEM 9

def find_max_scoring_num_rolls(num_rolls_averages):    
    """Finds number of dice from 1 to 10 in NUM_ROLLS_AVERAGES that gives the
       highest average score and returns it. If two numbers have the same
       average, the lower number of rolls will be returned.
    
    >>> num_rolls_averages = [3.2, 4.0, 7.8, 9.1, 8.9, 9.1, 8.1, 7.2, 6.1, 4.4]  
    >>> optimal_num_rolls = find_max_scoring_num_rolls(num_rolls_averages)
    >>> optimal_num_rolls
    4
    >>> num_rolls_averages = [3.2, 4.0, 7.8, 9.0, 8.9, 9.1, 8.1, 7.2, 6.1, 4.4]  
    >>> optimal_num_rolls = find_max_scoring_num_rolls(num_rolls_averages)
    >>> optimal_num_rolls
    6
    """
    max_num_rolls_average = max(num_rolls_averages)
    optimal_num_rolls = None
    found = False
    i = 0
    # Find first occurence of MAX_NUM_ROLLS_AVERAGE
    while not found and i < len(num_rolls_averages):
        # If current element is first occurence of MAX_NUM_ROLLS_AVERAGE
        if abs(num_rolls_averages[i] - max_num_rolls_average) < 0.01:
            optimal_num_rolls = i + 1
            found = True 
        i += 1 
    return optimal_num_rolls

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score) >= cutoff:
        verified_num_rolls = 0
    else:
        verified_num_rolls = num_rolls
    return verified_num_rolls
    # END PROBLEM 10


def swap_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least CUTOFF points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    free_bacon_points = free_bacon(opponent_score)
    
    potential_score = score + free_bacon_points

    swap = is_swap(potential_score, opponent_score)
    opponent_score_is_higher = opponent_score > potential_score
    beneficial_swap = swap and opponent_score_is_higher
    non_beneficial_swap = swap and not opponent_score_is_higher

    if beneficial_swap: 
        verified_num_rolls = 0
    elif (free_bacon_points >= cutoff) and not non_beneficial_swap:
        verified_num_rolls = 0
    else:
        verified_num_rolls = num_rolls 

    return verified_num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6  # Replace this statement
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
