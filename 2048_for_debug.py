import sys
import math
import random


def iprint(msg):
    print(f'{msg}', file=sys.stderr, flush=True)


def eprint(msg):
    print(f'{msg}', file=sys.stderr, flush=True)


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Board:
    __slots__ = ['seed', 'score', 'tiles', '__dict__']

    def __init__(self, seed, score, tiles=None):
        self.seed = seed
        self.score = score
        self.tiles = [] if tiles is None else tiles

    def get(self, id):
        result = [t for t in self.tiles if t.id == id]
        return result[0] if result else None

    def apply_move(self, d):
        is_move = False
        has_moved = False
        if d == 'L':
            for i in range(4):
                for j in range(1, 4):
                    t = self.get(j + 4 * i)
                    if t.val:
                        is_move = t.move_tile(self, d)
                        if not has_moved and is_move:
                            has_moved = True
        elif d == 'R':
            for i in range(4):
                for j in range(3)[::-1]:
                    t = self.get(j + 4 * i)
                    if t.val:
                        is_move = t.move_tile(self, d)
                        if not has_moved and is_move:
                            has_moved = True
        elif d == 'U':
            for j in range(4):
                for i in range(1, 4):
                    t = self.get(j + 4 * i)
                    if t.val:
                        is_move = t.move_tile(self, d)
                        if not has_moved and is_move:
                            has_moved = True
        elif d == 'D':
            for j in range(4):
                for i in range(3)[::-1]:
                    t = self.get(j + 4 * i)
                    if t.val:
                        is_move = t.move_tile(self, d)
                        if not has_moved and is_move:
                            has_moved = True
        return sum([t.val for t in self.tiles if t.merged]) if has_moved else -1

    def __repr__(self):
        result = ""
        for i in range(4):
            result += " ".join([str(t.val) for j, t in enumerate(self.tiles) if j // 4 == i]) + "\n"
        return result


class Tile:
    __slots__ = ['id', 'val', 'merged', '__dict__']

    def __init__(self, x, y, val, merged=None):
        self.id = x + 4 * y
        self.val = val
        self.merged = False if merged is None else merged

    def move_tile(self, b, d):
        stop = False
        t_next = b.get(self.id + moves[d])
        has_moved = False
        while t_next is not None:
            if t_next.val == 0:
                t_next.val, self.val = self.val, 0
                t = t_next
                t_next = b.get(t_next.id + moves[d])
                has_moved = True
                continue
            if t_next.val == self.val and not t_next.merged:
                t_next.val, self.val = self.val * 2, 0
                t_next.merged = True
                has_moved = True
                return has_moved
            return has_moved
        return has_moved

    def __repr__(self):
        return f'{self.id}/{self.val}'


def get_action(board):
    action_scores = []
    for d in moves:
        b = Board(board.seed, board.score)
        b.tiles = [Tile(t.id % 4, t.id // 4, t.val, t.merged) for t in board.tiles]
        score = b.apply_move(d)
        if score != -1:
            action_scores.append((score, d))
    eprint("Available actions: {}".format(action_scores))
    best_score = max(action_scores, key=lambda x: x[0])[0]
    best_moves = [(score, d) for score, d in action_scores if score == best_score]
    best_move = random.choice(best_moves)
    return best_move[1]


moves = {'U': -4, 'R': 1, 'D': 4, 'L': -1}
free_tiles = []
# Game loop
while True:
    free_tiles.clear()
    seed = int(input())  # needed to predict the next spawns
    score = int(input())
    iprint("Seed: {}".format(seed))
    iprint("Score: {}".format(score))

    board = Board(seed, score)

    for i in range(4):
        line = input()
        # iprint(line)
        for j, n in enumerate(line.split()):
            board.tiles.append(Tile(j, i, int(n)))

    eprint("\nInitial board")
    eprint(board)
    # eprint(board.tiles)

    # Calculate first action
    first_action = get_action(board)
    # update board
    board.apply_move(first_action)
    # Predict position/value of next tile in new board
    free_tiles = [t.id for t in board.tiles if not t.val]
    # eprint("Freetiles ({}) = {}".format(len(free_tiles), free_tiles))
    free_tiles.sort()   # In case of (already sorted)
    # eprint("Sorted freetiles ({}) = {}".format(len(free_tiles), free_tiles))
    # random.seed(seed)
    # spawnIndex = random.choice(free_tiles)
    spawnIndex = free_tiles[seed % len(free_tiles)]
    eprint("spawnIndex : {}".format(spawnIndex))
    # value = (seed & 0x10) == 0 ? 2 : 4
    t_seed = board.get(spawnIndex)
    # eprint("DEBUG : {}".format(int(bin(seed & 0x10), 2)))
    t_seed.val = 2 if int(bin(seed & 0x10), 2) == 0 else 4
    eprint("New tile: {}".format(t_seed))

    eprint("\nFirst Action: {}".format(first_action))
    eprint(board)

    # Calculate second action
    # second_action = get_action(board)
    # # update board
    # board.apply_move(second_action)
    # eprint("\nSecond Action: {}".format(second_action))
    # eprint(board)
    second_action = ''

    action = "{}{}".format(first_action, second_action)

    print(action)
