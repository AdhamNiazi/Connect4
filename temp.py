import random
import time
import pygame
import math
import sys
from copy import deepcopy
from connect4 import connect4
import pdb

ROW_COUNT = 6
COLUMN_COUNT = 7


class connect4Player(object):
    def __init__(self, position, seed=0, CVDMode=False):
        self.position = position
        self.opponent = None
        self.seed = seed
        random.seed(seed)
        if CVDMode:
            global P1COLOR
            global P2COLOR
            P1COLOR = (227, 60, 239)
            P2COLOR = (0, 255, 0)

    def play(self, env: connect4, move: list) -> None:
        move = [-1]


class human(connect4Player):

    def play(self, env: connect4, move: list) -> None:
        move[:] = [int(input('Select next move: '))]
        while True:
            if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
                break
            move[:] = [int(input('Index invalid. Select next move: '))]


class human2(connect4Player):

    def play(self, env: connect4, move: list) -> None:
        done = False
        while (not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.position == 1:
                        pygame.draw.circle(
                            screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
                    else:
                        pygame.draw.circle(
                            screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    move[:] = [col]
                    done = True


class randomAI(connect4Player):

    def play(self, env: connect4, move: list) -> None:
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        move[:] = [random.choice(indices)]


class stupidAI(connect4Player):

    def play(self, env: connect4, move: list) -> None:
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        if 3 in indices:
            move[:] = [3]
        elif 2 in indices:
            move[:] = [2]
        elif 1 in indices:
            move[:] = [1]
        elif 5 in indices:
            move[:] = [5]
        elif 6 in indices:
            move[:] = [6]
        else:
            move[:] = [0]


class minimaxAI(connect4Player):

    def play(self, env: 'connect4', move: list) -> None:
        board = deepcopy(env)
        best_move, eval = self.max_Player(board, depth=3)
        print("Final Move selected")
        print("BEST MOVE: ", best_move, "  EVAL: ", eval)
        move[:] = [best_move]

    def max_Player(self, env, depth):
        player = self.position
        if depth == 0:
            return None, self.score_board(env, self.position)

        max_eval = float('-inf')
        best_move = 3
        for col in range(COLUMN_COUNT):
            if self.isValidMove(env, col):
                board_copy = deepcopy(env)
                self.simulateMove(board_copy, col, self.position)
                _, eval = self.min_Player(board_copy, depth - 1)
                if (eval > max_eval):
                    max_eval = eval
                    best_move = col
                    print("MAX BEST MOVE: ", best_move, max_eval)
        return best_move, max_eval

    def min_Player(self, env, depth):
        player = self.opponent.position
        if depth == 0:
            return None, self.score_board(env, self.position)
        min_eval = float('inf')
        eval = float('inf')
        opp_best_move = 3
        for col in range(COLUMN_COUNT):
            if self.isValidMove(env, col):
                board = deepcopy(env)
                self.simulateMove(board, col, player)
                _, eval = self.max_Player(board, depth - 1)
                if (eval < min_eval):
                    min_eval = eval
                    opp_best_move = col
                    print("MIN BEST MOVE: ", opp_best_move, min_eval)
        return opp_best_move, min_eval

    def isValidMove(self, env, index):
        possible = env.topPosition >= 0
        if possible[index] == True:
            return True
        return False

    def simulateMove(self, env, col: int, player: int):
        env.board[env.topPosition[col]][col] = player
        env.topPosition[col] -= 1
        env.history[0].append(col)

    def score_board(self, board, player: int):
        score = 0
        opponent = 1
        if player == 1:
            opponent = 2

        score = self.evaluate(board, player)
        return score
        # score = self.getScore(board, player)
        # score -= self.getScore(board, opponent)
        # return score

    def evaluate(self, board, player):

        score = 0
        center_array = [int(i)for i in list(board.board[:, COLUMN_COUNT // 2])]
        center_count = self.count_occurrences(center_array, player)
        score += center_count * 2
        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board.board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, player)
        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board.board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, player)
        # Score positive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        return score

    def evaluate_window(self, window, player):
        score = 0
        opponent = 1
        if player == 1:
            opponent = 2

        if self.count_occurrences(window, player) == 4:
            score += MY_WIN
            return score
        elif self.count_occurrences(window, player) == 3 and self.count_occurrences(window, 0) == 1:
            score += THREE_VAL
        elif self.count_occurrences(window, player) == 2 and self.count_occurrences(window, 0) == 2:
            score += TWO_VAL

        if self.count_occurrences(window, opponent) == 4:
            score -= MY_WIN
            return score
        elif self.count_occurrences(window, opponent) == 3 and self.count_occurrences(window, 0) == 1:
            score -= THREE_VAL
        elif self.count_occurrences(window, opponent) == 2 and self.count_occurrences(window, 0) == 2:
            score -= TWO_VAL
        return score

    def count_occurrences(self, window, value):
        count = 0
        for element in window:
            if element == value:
                count += 1
        return count

    def getScore(self, board, player):

        # get Vertical scores this will be done by checking every possible win
        # and then adding them together based on the chance of this happening
        # , this is broken up into horizontal
        # vertical and diagnal

        # get row Col SCORING
        positionalScore = self.posScore(board, player)
        score = self.testAllFours(board, player)
        return positionalScore + score

    def testAllFours(self, board, player):
        # we first need to check all vertical possibilities
        # a possibility is a group of 4 spots on the board
        # by scoring groups of 4, we can be sure to know
        # whether we are about to win or how close we are
        for cols in range(COLUMN_COUNT):
            pass
        pass

    def posScore(self, board, player):
        score = 0
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if board.board[row][col] == player:
                    # print("ROW: ", row, "COL: ", col,"SVALUE THERE: ", BOARD_MULTIPLIER[row][col])
                    score += BOARD_MULTIPLIER[row][col]
        return score


class alphaBetaAI(connect4Player):

    def play(self, env: 'connect4', move: list) -> None:
        board = deepcopy(env)
        best_move, eval = self.max_Player(
            board, depth=4, alpha=float('-inf'), beta=float('inf'))
        print("BEST MOVE: ", best_move, "  EVAL: ", eval)
        move[:] = [best_move]

    def max_Player(self, env, depth, alpha, beta):
        player = self.opponent.position
        if depth == 0:
            return None, self.score_board(env, self.position)

        max_eval = float('-inf')
        best_move = 3
        for col in range(COLUMN_COUNT):
            if self.isValidMove(env, col):
                board_copy = deepcopy(env)
                self.simulateMove(board_copy, col, self.position)
                _, eval = self.min_Player(board_copy, depth - 1, alpha, beta)
                if (eval > max_eval):
                    max_eval = eval
                    best_move = col
                    print("MAX BEST MOVE: ", best_move, max_eval)
                alpha = max(max_eval, alpha)
                if alpha >= beta:
                    break
        return best_move, max_eval

    def min_Player(self, env, depth, alpha, beta):
        player = self.opponent.position
        if depth == 0:
            return None, self.score_board(env, self.position)
        min_eval = float('inf')
        eval = float('inf')
        opp_best_move = 3
        for col in range(COLUMN_COUNT):
            if self.isValidMove(env, col):
                board = deepcopy(env)
                self.simulateMove(board, col, player)
                _, eval = self.max_Player(board, depth - 1, alpha, beta)
                if (eval < min_eval):
                    min_eval = eval
                    opp_best_move = col
                    print("MIN BEST MOVE: ", opp_best_move, min_eval)
                beta = min(min_eval, beta)
                if alpha >= beta:
                    break
        return opp_best_move, min_eval

    def isValidMove(self, env, index):
        possible = env.topPosition >= 0
        if possible[index] == True:
            return True
        return False

    def simulateMove(self, env, col: int, player: int):
        env.board[env.topPosition[col]][col] = player
        env.topPosition[col] -= 1
        env.history[0].append(col)

    def score_board(self, board, player: int):
        score = 0
        opponent = 1
        if player == 1:
            opponent = 2

        score = self.evaluate(board, player)
        return score
        # score = self.getScore(board, player)
        # score -= self.getScore(board, opponent)
        # return score

    def evaluate(self, board, player):

        score = 0
        center_array = [int(i)for i in list(board.board[:, COLUMN_COUNT // 2])]
        center_count = self.count_occurrences(center_array, player)
        score += center_count * 2
        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board.board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, player)
        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board.board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, player)
        # Score positive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        return score

    def evaluate_window(self, window, player):
        score = 0
        opponent = 1
        if player == 1:
            opponent = 2

        if self.count_occurrences(window, player) == 4:
            score += MY_WIN
            return score
        elif self.count_occurrences(window, player) == 3 and self.count_occurrences(window, 0) == 1:
            score += THREE_VAL
        elif self.count_occurrences(window, player) == 2 and self.count_occurrences(window, 0) == 2:
            score += TWO_VAL

        if self.count_occurrences(window, opponent) == 4:
            score -= MY_WIN
            return score
        elif self.count_occurrences(window, opponent) == 3 and self.count_occurrences(window, 0) == 1:
            score -= THREE_VAL
        elif self.count_occurrences(window, opponent) == 2 and self.count_occurrences(window, 0) == 2:
            score -= TWO_VAL
        return score

    def count_occurrences(self, window, value):
        count = 0
        for element in window:
            if element == value:
                count += 1
        return count

    def checkVert(self, board, player):
        count = 0
        score = 0
        playerMultiplier = -5
        if player == self.position:
            playerMultiplier = 1
        available = False
        for cols in range(COLUMN_COUNT):
            rows = 5
            while rows >= board.topPosition[cols]:
                if rows == -1:
                    break
                if board.board[rows][cols] == player:
                    count += 1
                    rows -= 1
                elif board.board[rows][cols] == 0:
                    available = True
                    break
                else:
                    count = 0
                    break
            if count == 4:
                return MY_WIN
            elif count == 3:
                score += THREE_VAL
            elif count == 2:
                score += TWO_VAL
            elif count == 0:
                pass
            else:
                count += 1
            count = 0
        return score

    def posScore(self, board, player):
        score = 0
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if board.board[row][col] == player:
                    # print("ROW: ", row, "COL: ", col,"SVALUE THERE: ", BOARD_MULTIPLIER[row][col])
                    score += BOARD_MULTIPLIER[row][col]
        return score


SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
P1COLOR = (255, 0, 0)
P2COLOR = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

MY_WIN = 10000

WIN_VAL = 10000
THREE_VAL = 100
TWO_VAL = 4


# COL_MULTIPLIER = [.9, 1, 2, 4, 2, 1, .9]
BOARD_MULTIPLIER = [
    [1, 1, 2, 3, 2, 1, 1],
    [1, 1, 2, 9, 2,  1, 1],
    [1, 2, 4, 13, 4, 3, 1],
    [1, 5, 12, 18, 9, 5, 1],
    [1, 7, 12, 22, 13, 7, 1],
    [2, 9, 17, 30, 17, 9, 2]
]
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
"""

    def play(self, env: 'connect4', move: list) -> None:
        board = deepcopy(env)
        best_move, eval = self.max_Player(board, depth=3)
        print("Final Move selected")
        print("BEST MOVE: ", best_move, "  EVAL: ", eval)
        move[:] = [best_move]

    def max_Player(self, env, depth):
        player = self.position
        if depth == 0:
            return None, self.score_board(env, self.position)

        max_eval = float('-inf')
        best_move = 3
        for col in range(COLUMN_COUNT):
            if self.isValidMove(env, col):
                board_copy = deepcopy(env)
                self.simulateMove(board_copy, col, self.position)
                _, eval = self.min_Player(board_copy, depth - 1)
                if (eval > max_eval):
                    max_eval = eval
                    best_move = col
                    print("MAX BEST MOVE: ", best_move, max_eval)
        return best_move, max_eval

    def min_Player(self, env, depth):
        player = self.opponent.position
        if depth == 0:
            return None, self.score_board(env, self.position)
        min_eval = float('inf')
        eval = float('inf')
        opp_best_move = 3
        for col in range(COLUMN_COUNT):
            if self.isValidMove(env, col):
                board = deepcopy(env)
                self.simulateMove(board, col, player)
                _, eval = self.max_Player(board, depth - 1)
                if (eval < min_eval):
                    min_eval = eval
                    opp_best_move = col
                    print("MIN BEST MOVE: ", opp_best_move, min_eval)
        return opp_best_move, min_eval















def check_vertical(self, board, row, col, player: int):
        count = 0
        score = 0
        while row >= board.topPosition[col]:
            if board.board[row][col] == player:
                count += 1
                score = BOARD_MULTIPLIER[row][col]
                row -= 1
            elif board.board[row][col] == 0 and count != 1:
                score = 0
                break
            else:
                score = 0
                count = 0
                break

        if count == 4:
            return MY_WIN
        elif count == 3:
            return THREE_VAL
        elif count == 2:
            return TWO_VAL
        else:
            return score

 

def simulateUndoMove(self, env, col: int):
        r = 5
        while r > 0:
            if env.board[r-1][col] == 0:
                env.board[r][col] = 0
        env.board[0][col] = 0
        env.topPosition[col] += 1



def score_board(self, board, player: int):
        score = 0
        opponent = 1
        if player == 1:
            opponent = 2
        print("Player Board: ", player)
        score += self.check_sequences(board, player)
        print("Player Board: ", opponent)
        score -= self.check_sequences(board, opponent)
        print("SCORE: ", score)
        return score

    def check_sequences(self, board, player):
        score = 0
        win_found = False
        print(board.board)
        for i in reversed(range(ROW_COUNT)):
            for j in range(COLUMN_COUNT):
                if board.board[i][j] == player:
                    vert_score, win_found = self.check_vertical(
                        board, i-1, j, player, win_found)
                    horz_score, win_found = self.check_horizontal(
                        board, i, j, player, win_found)
                    diag_score, win_found = self.check_diagonal(
                        board, i, j, player, win_found)
                    score += vert_score + horz_score + diag_score
        print(player, " Score: ", score)
        return score

    def check_vertical(self, board, row, col, player: int, win_found):
        if win_found == True:
            return 0, True
        cur_score = 1
        count = 1
        while row >= 0:
            if board.board[row][col] == player:
                count += 1
                cur_score *= BOARD_MULTIPLIER[row][col]
                row -= 1
            elif board.board[row][col] == 0:
                break
            else:
                break

        # evaluate_Count()
        if count == 4:
            print("FOUND vertical WIN FOR: ", player)
            win_found = True
            return WIN_VAL, win_found
        elif count == 3:
            cur_score += THREE_VAL
        elif count == 2:
            cur_score += TWO_VAL
        return cur_score, win_found

    def check_horizontal(self, board, row, col, player: int, win_found):
        if win_found == True:
            return 0, True
        cur_score = 1
        count = 1
        next_empty = False
        prev_empty = False
        if col - 1 >= 0:
            if board.board[row][col-1] == 0:
                prev_empty = True
        while col < COLUMN_COUNT:
            if board.board[row][col] == player:
                count += 1
                cur_score *= BOARD_MULTIPLIER[row][col]
                col += 1
            elif board.board[row][col] == 0:
                next_empty = True
                break
            else:  # opponents piece
                break
        if count == 4:
            print("FOUND horizontal WIN FOR: ", player)
            return WIN_VAL, True
        elif count == 3:
            if prev_empty or next_empty:
                cur_score -= WIN_VAL
            cur_score += THREE_VAL
        elif count == 2:
            cur_score += TWO_VAL
        return cur_score, False

    def check_diagonal(self, board, row, col, player: int, win_found):
        if win_found == True:
            return 0, True
        count = 1
        cur_score = 1
        next_empty = False
        prev_empty = False
        if row < 5 and col > 0 and board.board[row + 1][col-1] != player:
            if board.board[row + 1][col-1] == 0:
                prev_empty = True
            # Check diagonal (top-right direction)
            i, j = row - 1, col + 1
            while i < ROW_COUNT and j < COLUMN_COUNT:
                if board.board[i][j] == player:
                    count += 1
                    cur_score *= BOARD_MULTIPLIER[i][j]
                    i -= 1
                    j += 1
                elif board.board[i][j] == 0:
                    next_empty = True
                    break
                else:
                    break
        if count == 4:
            print("FOUND diagnal WIN FOR: ", player)
            return WIN_VAL, True
        elif count == 3:
            if (prev_empty):  # not taking the win is just as bad as letting the opponent win
                return OPPONENT_WIN
            if (next_empty):
                return OPPONENT_WIN
            cur_score += THREE_VAL
        elif count == 2:
            cur_score += TWO_VAL

        count = 1
        if row < 5 and col < 6 and not board.board[row + 1][col+1] == player:
            i, j = row - 1, col - 1
            while i < ROW_COUNT and j > 0:
                if board.board[i][j] == player:
                    count += 1
                    cur_score *= BOARD_MULTIPLIER[i][j]
                    i -= 1
                    j -= 1
                elif board.board[i][j] == 0:
                    break
                else:
                    break

        if count == 4:
            print("FOUND diagnal WIN FOR: ", player)
            return WIN_VAL, True
        elif count == 3:
            cur_score += THREE_VAL
        elif count == 2:
            cur_score += TWO_VAL
        else:
            cur_score += count

        return cur_score, False
"""
