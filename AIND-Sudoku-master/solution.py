assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

### Update peers/units by adding diagonal constraints
new_peers=peers.copy()
new_units=units.copy()
diag_one = set(['A1','B2','C3','D4','E5','F6','G7','H8','I9'])
diag_one_list = [['A1','B2','C3','D4','E5','F6','G7','H8','I9']]
for each_diag_one in diag_one:
    assign_value(new_peers,each_diag_one,new_peers[each_diag_one].union(diag_one)-set([each_diag_one]))
    assign_value(new_units,each_diag_one,new_units[each_diag_one]+diag_one_list)
diag_two = set(['A9','B8','C7','D6','E5','F4','G3','H2','I1'])
diag_two_list = [['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
for each_diag_two in diag_two:
    assign_value(new_peers,each_diag_two,new_peers[each_diag_two].union(diag_two)-set([each_diag_two]))
    assign_value(new_units,each_diag_two,new_units[each_diag_two]+diag_two_list)

    
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return



def eliminate(values):
    for box in boxes:   ### Loop through every box in sudoku
        if len(values[box])>1:  ###Only check for boxes contain >1 possible solutions
            for peer in new_peers[box]: ### Check its peers and eliminate the possibilities
                if len(values[peer])==1:
                    value = values[box].replace(values[peer],'')
                    assign_value(values,box,value);
    return values



def only_choice(values):
    myflag=1
    ### myflag checks if there are new values updated to the sudoku
    ### if no new values were added, stop the loop
    while(myflag==1):
        myflag=0
        for box in boxes:   ###Loop through each box
            if len(values[box])>1:  ###Only check for boxes contain >1 possible solutions
                for unit in new_units[box]: ### Check for its unit(rows,cols,diagonals)
                    ### s is a string concatenate all numbers in the unit
                    s=""
                    for single_unit in unit:
                        if single_unit!=box:
                            for letter in values[single_unit]:
                                s=s+letter
                    ###If box contains unique character compare to s, its the only choice
                    for c in values[box]:   
                        if c not in s :
                            assign_value(values,box,c)
                            ### Update my flag if new values added to sudoku
                            myflag=1
    return values


                            
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values



def search(values):
    ### Reduce puzzle first
    values = reduce_puzzle(values)

    ### If no solution return false
    if values==False:
        return False

    ### Check if all boxes have only 1 solution
    correct = True
    for box in boxes:
        if len(values[box])!=1:
            correct = False
        ### Check if all units have number 1-9. Return false otherwise
        for unit in new_units[box]:
            mysum=set()
            for single_unit in unit:
                mysum.update(values[single_unit])
            if len(mysum)!=9:
                return False
    ### If solution is completed, return it
    if correct == True:
        return values     
    # Choose one of the unfilled squares with the fewest possibilities
    minlen = 9
    for box in boxes:
        if len(values[box])<minlen and len(values[box])>1:
            minlen = len(values[box])
            min_index = box
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[min_index]:
        temp = values.copy()
        assign_value(temp,min_index,digit)
        result = search(temp)
        if result :
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    ### String to Dictionary
    values = grid_values(grid)
    ### DFS embedded with elimination+only choice methods
    values = search(values)
    return values



def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for box in boxes: ### Loop through each box
        if len(values[box])==2: ### Only check for length 2 box
            for unit in units[box]: ### Find its twin by looping through the its units(row,cols)
                for single_unit in unit: ### For each rows, cols
                    nakedTwin = ""
                    if values[box]==values[single_unit] and box!=single_unit: ### Twin Found
                        nakedTwin = values[box]
                        for single_unit_inner in unit:  ### If twin found, update all other boxes in the unit
                            ###Box to be updated cannot be the twins themselves
                            if len(values[single_unit_inner])>1 and single_unit_inner!= single_unit and single_unit_inner!=box:
                               for c in nakedTwin:
                                   value = values[single_unit_inner].replace(c,'')
                                   assign_value(values,single_unit_inner,value)
    return values




if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

