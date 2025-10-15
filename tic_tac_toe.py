from copy import deepcopy

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
                                            # and board
Action = tuple[int, int]  # Where to place the player's piece

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state: State, player: int):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')

def alfa_beta_search(game:Game,state:State):
    player = game.to_move(state)
    _,move = max_value(game,state,player,float("-inf"),float("inf"))
    return move
def max_value(game: Game, state: State, player: int, alpha: float, beta: float) -> tuple[float, Action | None]:
    if game.is_terminal(state):
        return game.utility(state, player), None
    v = float("-inf")
    best: Action | None = None
    for a in game.actions(state):
        v2, _ = min_value(game, game.result(state, a), player, alpha, beta)
        if v2 > v:
            v, best = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            return v, best
    return v, best

def min_value(game:Game, state: State, player: int, alpha: float, beta: float) -> tuple[float, Action | None]:
    if game.is_terminal(state):
        return game.utility(state,player), None
    v = float("inf")
    best: Action | None = None
    for a in game.actions(state):
        v2, _ = max_value(game, game.result(state,a), player, alpha, beta)
        if v2 < v: 
            v, best = v2, a
            beta = min(beta, v)
        if v <= alpha:
            return v, best
    return v, best


def get_human_action(game: Game, state: State) -> Action:
    legal = set(game.actions(state))
    while True:
        s = input("Your move as 'row col' with 0–2 0–2: ").strip().split()
        if len(s) == 2 and all(t.isdigit() for t in s):
            a = (int(s[0]), int(s[1]))
            if a in legal:
                return a
        print("Invalid. Try again.")

# choose side: X=P1 or O=P2
side = input("Play as X (P1) or O (P2)? ").strip().lower()
human = 0 if side.startswith("x") else 1

game = Game()
state = game.initial_state()
game.print(state)

while not game.is_terminal(state):
    player = game.to_move(state)
    if player == human:
        action = get_human_action(game, state)
    else:
        action = alfa_beta_search(game, state)  # computer move
    print(f"P{player+1}'s action: {action}")
    state = game.result(state, action)
    game.print(state)
