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

        score = self.getScore(board, player)
        score -= self.getScore(board, opponent)
        return score

    def getScore(self, board, player):
        score = 0
        score += self.posScore(board, player)
        score += self.checkVert(board, player)
        score += self.checkHorizRight(board, player)
        score += self.checkdiagRight(board, player)
        score += self.checkPositiveDiagonal(board, player)
        return score

    def posScore(self, board, player):
        score = 0
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if board.board[row][col] == player:
                    score += BOARD_MULTIPLIER[row][col]
        return score

    def checkVert(self, board, player):
        score = 0
        for cols in range(COLUMN_COUNT):
            for rows in range(ROW_COUNT - 3):
                emptyCount = 0
                count = 0
                for row in range(rows, rows + 4):
                    if board.board[row][cols] == player:
                        count += 1
                    elif board.board[row][cols] == 0:
                        emptyCount += 1
                        break
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
                count = 0
        return score

    def checkHorizRight(self, board, player):
        score = 0
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                emptyCount = 0
                count = 0
                for c in range(col, col + 4):
                    if board.board[row][c] == player:
                        count += 1
                    elif board.board[row][c] == 0:
                        emptyCount += 1
                        break
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
        return score

    def checkdiagRight(self, board, player):
        score = 0
        for row in range(ROW_COUNT - 3):
            for col in range(3, COLUMN_COUNT):
                emptyCount = 0
                count = 0
                for i in range(4):
                    if board.board[row + i][col - i] == player:
                        count += 1
                    elif board.board[row + i][col - i] == 0:
                        emptyCount += 1
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
        return score

    def checkPositiveDiagonal(self, board, player):
        score = 0
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT - 3):
                emptyCount = 0
                count = 0
                for i in range(4):
                    if board.board[row + i][col + i] == player:
                        count += 1
                    elif board.board[row + i][col + i] == 0:
                        emptyCount += 1
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
        return score


class alphaBetaAI(connect4Player):

    def play(self, env: 'connect4', move: list) -> None:
        board = deepcopy(env)
        best_move, eval = self.max_Player(
            board, depth=4, alpha=float('-inf'), beta=float('inf'))
        move[:] = [best_move]

    def max_Player(self, env, depth, alpha, beta):
        player = self.position
        if depth == 0:
            return None, self.score_board(env, self.position)

        max_eval = float('-inf')
        best_move = 3
        for col in range(COLUMN_COUNT):
            if self.isValidMove(env, col):
                board_copy = deepcopy(env)
                self.simulateMove(board_copy, col, self.position)
                _, eval = self.min_Player(board_copy, depth - 1, alpha, beta)
                if (eval >= max_eval):
                    max_eval = eval
                    best_move = col
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
                if (eval <= min_eval):
                    min_eval = eval
                    opp_best_move = col
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

        score = self.getScore(board, player)
        score -= 2 * self.getScore(board, opponent)
        return score

    def getScore(self, board, player):
        score = 0
        score += self.posScore(board, player)
        score += self.checkVert(board, player)
        score += self.checkHorizRight(board, player)
        score += self.checkdiagRight(board, player)
        score += self.checkPositiveDiagonal(board, player)
        return score

    def posScore(self, board, player):
        score = 0
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if board.board[row][col] == player:
                    score += BOARD_MULTIPLIER[row][col]
        return score

    def checkVert(self, board, player):
        score = 0
        for cols in range(COLUMN_COUNT):
            for rows in range(ROW_COUNT - 3):
                emptyCount = 0
                count = 0
                for row in range(rows, rows + 4):
                    if board.board[row][cols] == player:
                        count += 1
                    elif board.board[row][cols] == 0:
                        emptyCount += 1
                        break
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
                count = 0
        return score

    def checkHorizRight(self, board, player):
        score = 0
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                emptyCount = 0
                count = 0
                for c in range(col, col + 4):
                    if board.board[row][c] == player:
                        count += 1
                    elif board.board[row][c] == 0:
                        emptyCount += 1
                        break
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
        return score

    def checkdiagRight(self, board, player):
        score = 0
        for row in range(ROW_COUNT - 3):
            for col in range(3, COLUMN_COUNT):
                emptyCount = 0
                count = 0
                for i in range(4):
                    if board.board[row + i][col - i] == player:
                        count += 1
                    elif board.board[row + i][col - i] == 0:
                        emptyCount += 1
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
        return score

    def checkPositiveDiagonal(self, board, player):
        score = 0
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT - 3):
                emptyCount = 0
                count = 0
                for i in range(4):
                    if board.board[row + i][col + i] == player:
                        count += 1
                    elif board.board[row + i][col + i] == 0:
                        emptyCount += 1
                    else:
                        break
                if count == 4:
                    return MY_WIN
                elif count == 3 and emptyCount == 1:
                    score += THREE_VAL
                elif count == 2 and emptyCount == 2:
                    score += TWO_VAL
                else:
                    pass
        return score


SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
P1COLOR = (255, 0, 0)
P2COLOR = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

MY_WIN = float('inf')
THREE_VAL = 100
TWO_VAL = 25


# COL_MULTIPLIER = [.9, 1, 2, 4, 2, 1, .9]
BOARD_MULTIPLIER = [
    [1, 1, 2, 3, 2, 1, 1],
    [1, 1, 2, 9, 2,  1, 1],
    [1, 2, 4, 13, 4, 3, 1],
    [1, 5, 8, 9, 8, 5, 1],
    [1, 7, 12, 14, 13, 7, 1],
    [1, 11, 20, 30, 20, 11, 1]
]
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
