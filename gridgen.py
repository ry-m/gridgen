import sys, random
import numpy as np
import tkinter as tk
import logging


# Logger
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
LOG = logging.Logger('dbg')


# Global variables (😳)
visited_cells = dict()
path = list()
final_grid = None

# Credit to The Coding Train (YouTube) for algorithm inspiration. 
# https://www.youtube.com/watch?v=m6-cm6GZ1iw/

class Move:
    """Determines a move in the NSEW direction i.e., up/down/right/left.
    """
    def __init__(self, dx, dy) -> None:
        self.dx = dx 
        self.dy = dy 
        self.tried = False
        
    def all_moves():
        """
        Returns:
            list[tuple]: all possible directions.
        """
        return [
            Move(0, 1),
            Move(0, -1),
            Move(1, 0), 
            Move(-1, 0)
        ]


class Cell:
    """A Cell is a node in the path. 
    """
    def __init__(self, x, y) -> None:
        self.x = x 
        self.y = y 
        self.clear()
        
    def clear(self):
        """'Resets' the cell to normal state. 
        """
        self.visited = False 
        self.options = Move.all_moves()
        
    def next_move(self):
        """Retrieve the next move in a random direction. The move must be possible. 

        Returns:
            Cell: the next neighbouring cell.
        """
        choices = [] 
        for o in self.options:
            nx, ny = (self.x + o.dx, self.y + o.dy)
            
            global visited_cells
            if not o.tried and not (nx, ny) in visited_cells:
                choices.append(o)
        
        # There are options, try one of them. 
        if len(choices) > 0:
            c = random.choice(choices)
            c.tried = True
            return Cell(self.x + c.dx, self.y + c.dy)
        
        # There are no options, must backtrack.
        LOG.debug('no next move determined')
        return None 
    
    def __repr__(self) -> str:
        return f'({self.x},{self.y})'


def generate_grid(i):
    xspan = (0, 0)
    yspan = (0, 0)
    
    current = Cell(0, 0) 
    path.append(current)
    visited_cells[(current.x, current.y)] = current 
    
    while len(path) < i: 
        # Determine the next move. 
        current = current.next_move() 
        
        # If there are no possible moves, backtrack.
        if current == None:
            LOG.debug('path is stuck, backtracking...')
            stuck = path.pop()
            stuck.clear() 
            current = path[len(path) - 1]
        # Otherwise, keep building the path.
        else:
            path.append(current) 
            visited_cells[(current.x, current.y)] = current 
            current.visited = True
            # Update the span, used to build the array.
            xspan = (
                min(xspan[0], current.x),
                max(xspan[1], current.x)
            )
            yspan = (
                min(yspan[0], current.y), 
                max(yspan[1], current.y)
            )
    
    # Building the array using the differences in xspan/yspan (arrays cannot be indexed 
    # negatively).
    global final_grid
    final_grid = np.zeros((1+(xspan[1] - xspan[0]), 1+(yspan[1] - yspan[0])), dtype=int)
    
    for move in path:
        xidx = move.x - xspan[0]
        yidx = move.y - yspan[0]
        final_grid[xidx, yidx] = 1
   
    
def display_grid():
    """Displays the grid to the user in a window using Tk. 
    """
    root = tk.Tk()
    root.title('gridgen')
    
    window_grid = [[tk.Label(root, width=1, height=1, bg='red') for _ in range(final_grid.shape[1])] for _ in range(final_grid.shape[0])]
    for x, y in np.ndindex(final_grid.shape):
        if (final_grid[x, y] == 1):
            window_grid[x][y].configure(bg='black')
        else:
            window_grid[x][y].configure(bg='white')
        window_grid[x][y].grid(row=x, column=y, padx=1, pady=1)
        
    root.mainloop()


# 'Main'
i = None
try:
    i = int(sys.argv[1])
    assert i >= 5 and i <= 50
except (IndexError, ValueError):
    print('usage: python3 gridgen.py [length: int]')
    sys.exit(1)
except AssertionError:
    print('error: length must be between 5 ans 50 inclusive')
    sys.exit(1)

if i:
    generate_grid(i)
    display_grid()
    