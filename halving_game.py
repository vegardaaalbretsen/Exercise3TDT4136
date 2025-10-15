#import math

"""Small two-player impartial game where players either decrement or halve a number.

This module implements a simple turn-based game used for demonstrating
minimax search. The game state is a tuple (player_index, number). Players
alternate turns; on each turn the current player chooses one of two actions:
  - '--'  : subtract 1 from the number
  - '/2'  : integer divide the number by 2 (floor division)

The player who makes the number reach 0 wins. The maximizer is always the
player whose turn it is when calling the search functions.

This file intentionally contains no external dependencies and aims to be
educational rather than optimized.
"""

State = tuple[int, int]
# State is (player_index, number_remaining)

Action = str
# Action is either '--' (decrement) or '/2' (halve with floor division)


class Game:
    """Represents the halving/decrement game.

    Attributes:
        N: initial number for the game.
    """

    def __init__(self, N: int):
        self.N = N

    def initial_state(self) -> State:
        """Return the initial state: player 0 to move, number = N."""
        return 0, self.N

    def to_move(self, state: State) -> int:
        """Return the index (0 or 1) of the player to move in the given state."""
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        """Return the list of legal actions from the state."""
        return ['--', '/2']

    def result(self, state: State, action: Action) -> State:
        """Return the state that results from applying action to state.

        The next player alternates (mod 2). Division uses integer floor division.
        """
        _, number = state
        if action == '--':
            return (self.to_move(state) + 1) % 2, number - 1
        else:
            return (self.to_move(state) + 1) % 2, number // 2  # Floored division

    def is_terminal(self, state: State) -> bool:
        """Return True when the game has ended (number reached zero)."""
        _, number = state
        return number == 0

    def utility(self, state: State, player: int) -> float:
        """Utility from the perspective of `player`.

        Must be called only for terminal states. Returns +1 if `player` is the
        winner, -1 otherwise.
        """
        assert self.is_terminal(state)
        return 1 if self.to_move(state) == player else -1

    def print(self, state: State):
        """Pretty-print a human-friendly description of the state."""
        _, number = state
        print(f'The number is {number} and ', end='')
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            else:
                print(f'P2 won')
        else:
            print(f'it is P{self.to_move(state)+1}\'s turn')


def minimax_search(game: Game, state: State) -> Action | None:
    """Return the best action for the player to move using minimax search.

    This is a simple full-depth minimax for the small game; it returns the
    action (string) or None if terminal.
    """
    player = game.to_move(state)
    _, move = max_value(game, state, player)
    return move

def max_value(game: Game, state: State, player: int) -> tuple[float, Action | None]:
    if game.is_terminal(state):
        return game.utility(state, player), None
    v = float("-inf")
    best: Action | None = None
    for a in game.actions(state):
        v2, _ = min_value(game, game.result(state, a), player)
        if v2 > v:
            v, best = v2, a
    return v, best

def min_value(game:Game, state: State, player: int) -> tuple[float, Action | None]:
    if game.is_terminal(state):
        return game.utility(state,player), None
    v = float("inf")
    best: Action | None = None
    for a in game.actions(state):
        v2, _ = max_value(game, game.result(state,a), player)
        if v2 < v: 
            v, best = v2, a
    return v, best
    
game = Game(5)

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state) # The player whose turn it is
                                         # is the MAX player
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)

# Expected output:
# The number is 5 and it is P1's turn
# P1's action: --
# The number is 4 and it is P2's turn
# P2's action: --
# The number is 3 and it is P1's turn
# P1's action: /2
# The number is 1 and it is P2's turn
# P2's action: --
# The number is 0 and P1 won