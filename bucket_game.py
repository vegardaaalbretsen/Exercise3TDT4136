"""Simple bucket-choice game used for demonstrating minimax.

State is represented as (player_index, actions), where `actions` is either
an array of bucket labels (strings) when the game is not terminal, or a
single-element list containing an integer reward when the game is terminal.

Available initial bucket choices are 'A', 'B', and 'C'. Choosing a bucket
replaces the actions list with the two numbers associated with that bucket.
When the actions list length becomes 1, the game is terminal and that single
integer represents the outcome (reward for the player who moved last).
"""

State = tuple[int, list[str | int]]
Action = str | int  # Bucket choice (as str) or choice of number


class Game:
    def initial_state(self) -> State:
        """Return the initial game state.

        The returned state is a tuple (player_index, actions). The starting
        player is 0 and the available actions are the bucket labels 'A','B','C'.
        """
        return 0, ['A', 'B', 'C']

    def to_move(self, state: State) -> int:
        """Return the index (0 or 1) of the player to move in `state`."""
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        """Return the list of legal actions from `state`.

        When non-terminal, this is a list of bucket labels; when terminal it
        is a single-element list containing the integer outcome.
        """
        _, actions = state
        return actions

    def result(self, state: State, action: Action) -> State:
        """Apply `action` to `state` and return the resulting state.

        If `action` is a bucket label ('A','B','C'), return the two-number
        list associated with that bucket. If `action` is an integer, it is
        treated as a terminal reward and becomes a single-element action list.
        """
        if action == 'A':
            return (self.to_move(state) + 1) % 2, [-50, 50]
        elif action == 'B':
            return (self.to_move(state) + 1) % 2, [3, 1]
        elif action == 'C':
            return (self.to_move(state) + 1) % 2, [-5, 15]
        assert type(action) is int
        return (self.to_move(state) + 1) % 2, [action]

    def is_terminal(self, state: State) -> bool:
        """Return True when `state` is terminal (only one action left)."""
        _, actions = state
        return len(actions) == 1

    def utility(self, state: State, player: int) -> float:
        """Return utility value for `player` in a terminal `state`.

        The state's single integer is the reward for the player who moved
        last; the opponent receives the negated value (zero-sum semantics).
        """
        assert self.is_terminal(state)
        _, actions = state
        assert type(actions[0]) is int
        return actions[0] if player == self.to_move(state) else -actions[0]

    def print(self, state: State):
        """Pretty-print a human-friendly description of `state`."""
        print(f'The state is {state} and ', end='')
        if self.is_terminal(state):
            print(f'P1\'s utility is {self.utility(state, 0)}')
        else:
            print(f'it is P{self.to_move(state)+1}\'s turn')

def minimax_search(game: Game, state: State) -> Action | None:
    """Perform a full-depth minimax search and return the selected action.

    Returns None for terminal states.
    """
    player = game.to_move(state)
    _, move = max_value(game, state, player)
    return move
def max_value(game: Game, state: State, player: int) -> tuple[float, Action | None]:
    """Return the (value, best_action) for the maximizing player.

    This is the standard recursive maximizer used by minimax.
    """
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
    """Return the (value, best_action) for the minimizing player.

    Note: this implementation mirrors the typical minimax minimizer.
    """
    if game.is_terminal(state):
        return game.utility(state,player), None
    v = float("-inf")
    best: Action | None = None
    for a in game.actions(state):
        v2, _ = max_value(game, game.result(state,a), player)
        if v2 > v:
            v, best = v2, a
    return v, best

game = Game()

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
