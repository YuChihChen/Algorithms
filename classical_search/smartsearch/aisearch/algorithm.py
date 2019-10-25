""" 
This code was adapted from https://github.com/aimacode/aima-python
    note: & ABC & means the sentence 'ABC' are comming from the reference above

Author : Albert Chen

This moudle will provide uninform and inform search algorithms  
"""
import numpy as np
from collections import deque
from structure import Problem
from structure import Node
from structure import AQueue




#######################################################################################
#                             Uninform Search Algorithm                               #
#######################################################################################

# =================================== Tree Search ===================================
def tree_search(problem, mode):
    frontier = AQueue(mode) 
    frontier([Node(state=problem.initial)])
    while frontier.empty():
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None




# =================================== Graph Search ===================================













#######################################################################################
#                               inform Search Algorithm                               #
#######################################################################################













if __name__ == '__main__':
    # This class is from the reference above, which is used for testing algorithms only
    class NQueensProblem(Problem):
        """ The problem of placing N queens on an NxN board with none attacking
        each other.  A state is represented as an N-element array, where
        a value of r in the c-th entry means there is a queen at column c,
        row r, and a value of -1 means that the c-th column has not been
        filled in yet.  We fill in columns left to right.
        >>> depth_first_tree_search(NQueensProblem(8))
        <Node (7, 3, 0, 2, 5, 1, 6, 4)>
        """

        def __init__(self, N):
            self.N = N
            self.initial = tuple([-1] * N)
            Problem.__init__(self, self.initial)

        def actions(self, state):
            """ In the leftmost empty column, try all non-conflicting rows. """
            if state[-1] is not -1:
                return []  # All columns filled; no successors
            else:
                col = state.index(-1)
                return [row for row in range(self.N)
                        if not self.conflicted(state, row, col)]

        def transition(self, state, row):
            """Place the next queen at the given row."""
            col = state.index(-1)
            new = list(state[:])
            new[col] = row
            return tuple(new)

        def conflicted(self, state, row, col):
            """Would placing a queen at (row, col) conflict with anything?"""
            return any(self.conflict(row, col, state[c], c)
                    for c in range(col))

        def conflict(self, row1, col1, row2, col2):
            """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
            return (row1 == row2 or  # same row
                    col1 == col2 or  # same column
                    row1 - col1 == row2 - col2 or  # same \ diagonal
                    row1 + col1 == row2 + col2)  # same / diagonal

        def goal_test(self, state):
            """Check if all columns filled, no conflicts."""
            if state[-1] is -1:
                return False
            return not any(self.conflicted(state, state[col], col)
                        for col in range(len(state)))

        def h(self, node):
            """Return number of conflicting queens for a given node"""
            num_conflicts = 0
            for (r1, c1) in enumerate(node.state):
                for (r2, c2) in enumerate(node.state):
                    if (r1, c1) != (r2, c2):
                        num_conflicts += self.conflict(r1, c1, r2, c2)
            return num_conflicts
    
    def state_to_matrix(state, N):
        M = np.zeros((N, N), np.int32)
        for j in range(N):
            i = state[j]
            M[i][j] = 1
        return M

    N = 8
    QnProblem = NQueensProblem(N)
    
    goal_node = tree_search(QnProblem, 'FILO')
    print('================== DFS ==================')
    print(state_to_matrix(goal_node.state, N))
    print('\n')

    print('================== BFS ==================')
    goal_node = tree_search(QnProblem, 'FIFO')
    print(state_to_matrix(goal_node.state, N))
    print('\n')