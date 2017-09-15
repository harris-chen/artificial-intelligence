# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To solve the naked twins problem, I first search for naked twins in the puzzle.
I did this by searching all twins in a unit for all boxes, and these are used to exclude possibilities in other squares in the same group.
Naked twins method is similar to elimination and only-choice methods, we can extract the information and further eliminate some possible solutions.
By applying them to constraint propagation, we greatly reduced the search space before we apply the DFS technique to solve the puzzle.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: For diagonal sudoku problem, I used the same concecpt that was taught in the lesson except that I extended the peers and units for each diagonal elements. 
I first implemented the elimination method, i.e, if a box has a value assigned, then non of its peers can have the same value.
Then i used the only-choice method: If there is only one box in a unit which would allow a certain digit, then that box must be assigned that digit.
By using the above 2 methods, I drastically reduced the search space, making it an effective AI technique.
Then I picked a box with a minimal number of possibilities, recursively solve sudoku with DFS techniques, I have implemented a fast and efficient AI solver.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

