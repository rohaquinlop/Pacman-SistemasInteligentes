# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import queue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # Robin's code
    initialState = problem.getStartState()

    stack = util.Stack()
    state = [initialState, [], [initialState]]  # Coords, actions
    ans = []

    stack.push(state)

    while not stack.isEmpty():
        # Check if the state is a goal state
        state = stack.pop()
        coords = state[0]

        if problem.isGoalState(coords):
            return state[1]

        succesors = problem.getSuccessors(coords)

        for successor in succesors:
            coord = successor[0]
            action = successor[1]

            if coord not in state[2]:
                newState = (coord, state[1] + [action], state[2] + [coord])
                stack.push(newState)
    return ans


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    initialState = problem.getStartState()

    ans = []
    queue = util.Queue()
    state = [initialState, []]  # Coords, actions
    visited = dict()
    visited[initialState] = True

    queue.push(state)

    while not queue.isEmpty():
        state = queue.pop()

        coords = state[0]
        actions = state[1]

        if problem.isGoalState(coords):
            ans = actions
            break

        successors = problem.getSuccessors(coords)
        for successor in successors:
            coord = successor[0]
            action = successor[1]

            if coord not in visited:
                visited[coord] = True
                newState = (coord, actions + [action])
                queue.push(newState)

    return ans


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    ans = []

    initialState = problem.getStartState()
    pq = util.PriorityQueue()
    visited = dict()
    pq.push((initialState, [], 0), 0)
    visited[initialState] = 0

    while not pq.isEmpty():
        state = pq.pop()
        coords = state[0]
        actions = state[1]
        actCost = state[2]

        if problem.isGoalState(coords):
            ans = actions
            break

        successors = problem.getSuccessors(coords)

        for successor in successors:
            coord = successor[0]
            action = successor[1]
            cost = successor[2]

            if coord not in visited:
                visited[coord] = actCost + cost
                newState = (coord, actions + [action], cost + actCost)
                pq.push(newState, cost + actCost)
            elif cost + actCost < visited[coord]:
                newState = (coord, actions + [action], cost + actCost)
                pq.push(newState, cost + actCost)
    return ans


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ans = []
    visited = dict()
    pq = util.PriorityQueue()

    initialState = (problem.getStartState(), [])
    pq.push(initialState, 0)
    visited[problem.getStartState()] = 0

    while not pq.isEmpty():
        state = pq.pop()
        pos = state[0]
        actions = state[1]

        if problem.isGoalState(pos):
            ans = actions
            break

        successors = problem.getSuccessors(pos)

        for successor in successors:
            s, a, c = successor
            cost = visited[pos] + c
            if s not in visited or cost < visited[s]:
                visited[s] = cost
                priority = cost + heuristic(s, problem)
                newState = (s, actions + [a], cost)
                pq.push(newState, priority)
    return ans


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
