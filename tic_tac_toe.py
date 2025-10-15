from copy import deepcopy
import time

State = tuple[int, list[list[int | None]]]
Action = tuple[int, int]

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])
    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index
    def actions(self, state: State) -> list[Action]:
        _, board = state
        return [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
    def result(self, state: State, action: Action) -> State:
        _, board = state
        r, c = action
        nb = deepcopy(board)
        nb[r][c] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, nb
    def is_winner(self, state: State, player: int) -> bool:
        _, b = state
        rows = any(all(b[r][c] == player for c in range(3)) for r in range(3))
        cols = any(all(b[r][c] == player for r in range(3)) for c in range(3))
        diag = all(b[i][i] == player for i in range(3)) or all(b[i][2-i] == player for i in range(3))
        return rows or cols or diag
    def is_terminal(self, state: State) -> bool:
        _, b = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(b[r][c] is not None for r in range(3) for c in range(3))
    def utility(self, state: State, player: int):
        assert self.is_terminal(state)
        if self.is_winner(state, player): return 1
        if self.is_winner(state, (player + 1) % 2): return -1
        return 0
    def print(self, state: State):
        _, b = state
        print()
        for r in range(3):
            cells = [(' ' if b[r][c] is None else 'x' if b[r][c] == 0 else 'o') for c in range(3)]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if r < 2: print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0: print('P1 won')
            elif self.utility(state, 1) > 0: print('P2 won')
            else: print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')

# -------- Minimax (no pruning) --------
def minimax_search(game: Game, state: State) -> Action | None:
    player = game.to_move(state)
    v, move = _max_plain(game, state, player)
    return move

def _max_plain(game: Game, state: State, player: int) -> tuple[float, Action | None]:
    if game.is_terminal(state): return game.utility(state, player), None
    v, best = float("-inf"), None
    for a in game.actions(state):
        v2, _ = _min_plain(game, game.result(state, a), player)
        if v2 > v: v, best = v2, a
    return v, best

def _min_plain(game: Game, state: State, player: int) -> tuple[float, Action | None]:
    if game.is_terminal(state): return game.utility(state, player), None
    v, best = float("inf"), None
    for a in game.actions(state):
        v2, _ = _max_plain(game, game.result(state, a), player)
        if v2 < v: v, best = v2, a
    return v, best

# -------- Alpha–beta --------
def alfa_beta_search(game: Game, state: State) -> Action | None:
    player = game.to_move(state)
    _, move = _max_ab(game, state, player, float("-inf"), float("inf"))
    return move

def _max_ab(game: Game, state: State, player: int, alpha: float, beta: float) -> tuple[float, Action | None]:
    if game.is_terminal(state): return game.utility(state, player), None
    v, best = float("-inf"), None
    for a in game.actions(state):
        v2, _ = _min_ab(game, game.result(state, a), player, alpha, beta)
        if v2 > v:
            v, best = v2, a
            alpha = max(alpha, v)
        if v >= beta: break
    return v, best

def _min_ab(game: Game, state: State, player: int, alpha: float, beta: float) -> tuple[float, Action | None]:
    if game.is_terminal(state): return game.utility(state, player), None
    v, best = float("inf"), None
    for a in game.actions(state):
        v2, _ = _max_ab(game, game.result(state, a), player, alpha, beta)
        if v2 < v:
            v, best = v2, a
            beta = min(beta, v)
        if v <= alpha: break
    return v, best

# -------- Timing first move and auto vs auto --------
game = Game()
s0 = game.initial_state()

# time plain minimax first move
t0 = time.perf_counter()
m_plain = minimax_search(game, s0)
t1 = time.perf_counter()

# time alpha–beta first move
t2 = time.perf_counter()
m_ab = alfa_beta_search(game, s0)
t3 = time.perf_counter()

print(f"First move (minimax): {m_plain}, time: {(t1 - t0)*1000:.3f} ms")
print(f"First move (alpha–beta): {m_ab}, time: {(t3 - t2)*1000:.3f} ms")

# play computer vs computer using alpha–beta
state = deepcopy(s0)
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = alfa_beta_search(game, state)
    print(f"P{player+1}'s action: {action}")
    state = game.result(state, action)
    game.print(state)
