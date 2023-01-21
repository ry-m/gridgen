# gridgen
Self-avoiding random walk algorithm to be used in a game

## What is this?
The Self-Avoiding Walk is a computer science problem for generating a random path with finite directions (or 'choices'). Games use this concept to procedurally generate paths. There is no known formula to deterministically solve the problem.

## My implementation 
The Python file generates a random path in a grid context, where the next move can be either N, S, E, or W. If there is no possible option, it 'backtracks'. The path is stored dynamically with negative indices, but in the final stage, it is translated to a fixed-size array that can be managed more easily. 

The algorithm is a brute-force algorithm as there is no deterministic solution to the problem. Therefore, it is unstable when the size increases. 

The grid is displayed graphically to the user. 

## Usage

`python3 gridgen.py [size]`

where size is between 5 and 50 inclusive. This limitation is due to the grid's infinite size during the generation process.
