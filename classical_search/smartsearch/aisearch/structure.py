""" 
This code was adapted from https://github.com/aimacode/aima-python
    note: & ABC & means the sentence 'ABC' are comming from the reference above

Author : Albert Chen

This moudle will provide data structure and abstract class for search problems 
"""





# ============================= abstract class: Problem =============================
""" 
Problem class is an abstract class. From this class, we will know how to operate states
, evaluate cost and how to conduct goal test. They are one single step operations. 

For using these operations smartly to reach our goal, we need an efficient algorithm.
For coding an efficient algorithm, we need a good data struct, Node, which will be
implimented in the next class.
"""
class AbstractProblem(object):
    """ 
    The essential parts of a search problem: SCATTER
        S -> States        : initial and goal states 
        C -> Constraints   : constraints of states or actions
        A -> Actions       : avalible actions for a state 
        T -> Transition    : n' of n -> a -> n'
        T -> Goal Test     : test if a state is the goal of the problem 
        E -> Evaluate Cost : the spending cost from one state to another  
        R -> Result        : final results of path
    """
    def __init__(self, initial, goal=None):
        """ S : States
        Initial and goal states with Node data structure 
        """
        self.initial = initial
        self.goal = goal
    
    def constraints(self, state=None, action=None):
        """ C: Constraints
        Check if a state or a action is legal 
        """
        if state is None and action is None:
            return True
        if state is not None:
            raise NotImplementedError
        if action is not None:
            raise NotImplementedError

    def actions(self, state):
        """ A: Actions
        Given a state, return all avaliable actions. 
        & The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once. & 
        """
        raise NotImplementedError

    def transition(self, state, action):
        """ T: Transition
        Give a state and an action, this function will do:
        1. check if the action is in self.actions(state)
        2. return a child state that results from the action acting on the state
        """
        raise NotImplementedError

    def goal_test(self, state):
        """ T: Goal Test
        & Return true if the state is a goal. 
        The default method compares the state to self.goal or 
        checks for state in self.goal if it is alist, as specified in the constructor. 
        Override this method if checking against a single self.goal is not enough. & """
        return state in self.goal

    def cost(self, state1, action, state2):
        """ E: Evaluate Cost
        return the spending cost of an action: state1 --> state2
        """
        return 1
    
    def result(self):
        """ R: Result
        to save the best avaliable path if the result is to find a best path 
        """
        pass

    def value(self, state):
        """
        For optimization problem, each state will have a value. 
        The seach problem is to find a state having the minimum(maximum) value.
        """
        raise NotImplementedError

    def heuristic_function(self, state):
        """ return h(state) in A* search"""
        raise NotImplementedError





# ============================= data struct: Node =============================
""" 
Node class is an data structure. You do not need to subcalss this class. 
As metioned before, for coding our search algorithms efficiently, we need a good data 
structure, that is the Node. The Node is basically desgined for tree search, that is, 
we can have some Nodes that have the same states but with different paths from root to 
the Node. For the purpose of graph search, we will need to adapte this class.

Note: For the attributes that depends on a state only (path independ), e.q. h(n), 
will be implimented in the class of State.   
"""
class Node:
    """ & A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. & """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """ Create a new Node from tree search; action: parent -> self(Node) 
            After inheriting AbstractNone, you may want to implement g(Node) """
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = parent.depth + 1 if parent else 0
        self.g = path_cost

    def __repr__(self):
        return f'<Node: {self.state};  Paraent: {self.parent};  Action: {self.action}>'

    def expand(self, problem):
        """ List nodes that are reachable from this node in a single step. """
        nodes = [self.child_node(problem, action) for action in problem.actions(self.state)]
        return nodes

    def child_node(self, problem, action):
        """ Create a child Node after conducting an action on self.state. """
        child_state = problem.transition(self.state, action)
        child_path_cost = self.g + problem.cost(self.state, action, child_state)
        return Node(child_state, self.state, action, child_path_cost)

    def path_actions(self):
        """ & Return the sequence of actions to go from the root to this node. &"""
        return [node.action for node in self.path_nodes()]
    
    def path_nodes(self):
        """ & Return the sequence of nodes to go from the root to this node. & """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # & We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.] &

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.state == other.state

    def __hash__(self):
        return hash(self.state)





