# Nonogram Solver
Nonogram is a game in which a player must fill in a grid with different colored squares to create a pattern. What this pattern is is not explicitly provided to the player but is instead suggested through clues that the player must unpack.

Explanation of how to play:
https://puzzlygame.com/pages/how_to_play_nonograms/

The files in this repository find the solutions to randomly generated nonogram puzzles through efficient use of tree-based pattern generation.

## The Nonogram
The randomly generated nonograms are created using the `new_grid` function. This function creates a nonogram solution by creating a grid based on a pre-determined width and height, and creates a solution by filling in a pre-determined percentage of the grid's cells. The amount of colors used in the solution is determined by the amount of colors in the `colors` list. This list is meant to be altered by those who are running the code and already has color values that can be added by removing the notation leaving them as comments. This solution is not directly provided to the player nor solver but is suggested to them through clues corresponding to the rows and columns of the solution.

![image](https://github.com/user-attachments/assets/d61ed409-57fc-401d-83c7-26d1e66cd5c1)

## Solver With Playing
The file under the name `solver-display.py` creates a playable nonogram experience and display of the solver using the pygame library.

### Playable Nonogram
To change a cell's value, the player can click on the cell. Clicking on the cell will loop through the possible states of the cell, with the first being a blank (zero), the last being a definite zero (displayed as grey but traditionally represented as an 'X'), and all other states being all other colors used. Should an input of a column or row match the clues provided, a green square will be displayed at the end of that row or column. Should the player want to reset their grid so that all cells are once again blank, they may press the 'r' key to do so. Due to how the nonograms are generated, it is possible for a nonogram to have more than one solution. While it is possible to create one with only one solution, this program does not since that would make the nature of the solver redundant. Should the interactable grid have a viable solution, the grid will reset with a new generated nonogram.

### The Solver
To toggle the solver on and off, a player can press the 'p' key. Once toggled on, the solver uses the `ai_run` function to find solutions to the nonogram. This function splits the grid into columns and rows and then finds all possible solutions to those columns or rows based on their previous inputs. After these possible solutions are generated, the algorithm "overlaps" them to see which cells always have a concsistent value. Since possible solutions are found based on data already inputted, the cross-sections of columns and rows allow for new data to be processed by those columns or rows in the next run-through. The possible solutions are created in a tree where each branch is a list in which either a '1' or a '0' is added. The '1' represents an addition of a clue whereas a '0' represents a blank/empty cell. Should any values in these branches not align with the data taken in, that branch is pruned, allowing for a far more efficient algorithm. Should a nonogram have more than one solution, the solver will need a "hint" to finish solving. A "hint" is when a random unmarked cell is set to it's solution. This allows for more transparency of when a human player would decide on a possible solution and when an algorithm would traditionally start guessing. Once the solver finds the solution, the grid and solutions are reset, and the cycle repeats.

## Solver With Only Results
The file under the name `solver-only-results.py` runs the solver without a pygame display. This file uses the same `ai_run` function as the display file does and uses the exact same method of solving as well. Although, this solver begins as soon as the program is run and upon finding a solution, the amount of time taken to find the solution as well as the number of hints used for that solve is printed. This solver runs infinitely and resets the grid and solution every time that a solution is found.
