# Hog

Hog is a Python Command-Line program designed and implemented to simulate the dice game Hog and support the usage of various strategies.

## Rules

In Hog, two players alternate turns trying to be the first to end a turn with at least 100 total points. On each turn, the current player 
chooses some number of dice to roll, up to 10. That player's score for the turn is the sum of the dice outcomes. However, a player who 
rolls too many dice risks:

- **Pig Out**. If any of the dice outcomes is a 1, the current player's score for the turn is 1. 
<details><summary>Examples</summary>
  <ol>
    <li>The current player rolls 7 dice, 5 of which are 1's. They score 1 point for the turn.</li>
    <li>The current player rolls 4 dice, all of which are 3's. Since Pig Out did not occur, they score 12 points for the turn.</li>
  </ol>
</details>

In a normal game of Hog, Pig Out is the only rule. However, to spice up the game, we'll include some special rules:

- **Free Bacon**. A player who chooses to roll zero dice scores points equal to ten minus the value of the opponent score's ones digit, 
  summed with the value of the opponent's score's tens digit.
<details>
  <summary>Examples</summary>
    <ol>
      <li>The opponent has a score of 32, and the current player rolls zero dice. The current player will receive 10 - 2 + 3 = 11 points.</li>
      <li>The opponent has a score of 19, and the current player rolls zero dice. The current player will receive 10 - 9 + 1 = 2 points.</li>
      <li>The opponent has a score of 80, and the current player rolls zero dice. The current player will receive 10 - 0 + 8 = 18 points.</li>
      <li>The opponent has a score of 5, and the current player rolls zero dice. The current player will receive 10 - 5 + 0 = 5 points.</li>
    </ol>
</details>

- **Feral Hogs**. If the number of dice the current player rolls is exactly 2 away from the number of points they scored on the previous turn, 
  they get 3 extra points for the turn. 
<details>
  <summary>Examples</summary>
    <ol>
      <li>
        <ul>
          <li>Both players start out at 0. (0, 0)</li>
          <li>Player 0 rolls 3 dice and gets 7 points. (7, 0)</li>
          <li>Player 1 rolls 1 dice and gets 4 points. (7, 4)</li>
          <li>Player 0 rolls 5 dice and gets 10 points. 5 is 2 away from 7, so player 0 gets a bonus of 3. (20, 4)</li>
          <li>Player 1 rolls 2 dice and gets 8 points. 2 is 2 away from 4, so player 1 gets a bonus of 3. (20, 15)</li>
          <li>Player 0 rolls 8 dice and gets 20 points. 8 is 2 away from 10, so player 0 gets a bonus of 3. (43, 15)</li>
          <li>Player 1 rolls 6 dice and gets 1 point. 6 is 2 away from 8, so player 1 gets a bonus of 3. (43, 19)</li>
        </ul>
      </li>
      <li>
        <ul>
          <li>Both players start out at 0. (0, 0)</li>
          <li>Player 0 rolls 2 dice and gets 3 points. 2 is 2 away from 0, so player 0 gets a bonus of 3. (6, 0)</li>
        </ul>
      </li>
    </ol>
</details>

- **Swine Swap**. After points for the turn are added to the current player's score, if the absolute value of the difference between the current 
  player score's ones digit and the opponent score's ones digit is equal to the value of the opponent score's tens digit, the scores should be 
  swapped. **A swap may occur at the end of a turn in which a player reaches the goal score, leading to the opponent winning**.
<details>
  <summary>Examples</summary>
    <ol>
      <li>
        At the end of the first player's turn, the players have scores of 6 and 2. The difference in the ones digits is 6 - 2 = 4, and 4 != 0 
        (which is the tens digit of the second player), so no swap occurs.
      </li>
      <li>
        At the end of the first player's turn, the players have scores of 17 and 65. The difference in the ones digits is 7 - 5 = 2, and 2 != 6 
        (which is the tens digit of the second player), so no swap occurs.
      </li>
      <li>
        At the end of the first player's turn, the players have scores of 55 and 23. The difference in the ones digits is 5 - 3 = 2, and 2 == 2 
        (which is the tens digit of the second player), so the scores are swapped.
      </li>
      <li>
        At the end of the first player's turn, the players have scores of 89 and 54. The difference in the ones digits is 9 - 4 = 5, and 5 == 5 
        (which is the tens digit of the second player), so the scores are swapped.
      </li>
    </ol>
</details>

## Getting Started

### Installation

1. Install the ```Hog``` archive by downloading [```Hog-master.zip```](https://github.com/tchitete1/Hog/archive/master.zip)
2. Open a new terminal window in the directory where the archive was downloaded
3. Unzip the archive using the following command to obtain the ```Hog-master``` directory:
```
unzip Hog-master.zip
```
4. Change into the ```Hog-master``` directory by executing the following command:
```
cd Hog-master
```

### Execution

* To execute ```Hog```, execute the following:
```
python3 hog_gui.py 
```

## Author

Tanaka Chitete
* [Linkedin](https://www.linkedin.com/in/tanaka-chitete/)

## Acknowledgments

* Thank you to [DomPizzie](https://github.com/DomPizzie) for the [template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
