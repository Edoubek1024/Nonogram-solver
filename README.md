# Nonogram Solver
Nonogram is a game in which a player must fill in a grid with different colored squares to create a pattern. What this pattern is is not explicitly provided to the player but is instead suggested through hints that the player must unpack.

Explanation of how to play:
https://puzzlygame.com/pages/how_to_play_nonograms/

The files in this repository find the solutions to randomly generated nonogram puzzles through efficient use of tree-based pattern generation.

## The Nonogram
The randomly generated nonograms are created using the `new_grid` function. This function creates a nonogram solution by creating a grid based on a pre-determined width and height, and creates a solution by filling in a pre-determined percentage of the grid's cells. The amount of colors used in the solution is determined by the amount of colors in the `colors` list. This list is meant to be altered by those who are running the code and already has color values that can be added by removing the notation leaving them as comments. This solution is not directly provided to the player nor solver but is suggested to them through hints corresponding to the rows and columns of the solution.

## Solver With Playing
The file under the name `solver-display.py` creates a playable nonogram experience.

## Solver With Only Results
