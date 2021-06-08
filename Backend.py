import logging
import random
import time


class TicToe:
    def __init__(self, size):
        # default symbol which is always starting
        self.symbol = "O"
        # size of board
        self.size = size

        # if sb won or it's draw - it will change to "X", "O" or "_" - if it's draw
        self.game_status = None
        # if sb won the game, it will change to "X" or "O"
        # self.win = None
        # if it's draw it will change to True
        # self.draw = False

        # First index - what type of win: 0 - horizontal, 1 - vertical, 2 - crossing left top, 3 - crossing right top
        # Second index - row or column or first index of crossing win
        self.win_coordinates = [None, None]

        # whole board. If field is empty it will have '_', if it's occupied it will have "O" or "X"
        self.board = []
        # self.main_menu()
        for j in range(self.size):
            self.board.append([])
            for k in range(self.size):
                self.board[j].append("_")

        # for testing
        self.hard_moves_amount = 0
        self.max_depth = 0
        # self.board = [["X", "_", "X"], ["O", "X", "O"], ["_", "_", "O"]]
        # size = 6

        """self.board = [['X', 'X', 'X', 'X', 'O', 'O'], ['X', 'X', 'X', 'X', 'O', 'O'], ['X', 'X', 'X', 'O', 'O', 'O'],
                      ['_', '_', 'O', '_', 'O', 'O'], ['_', '_', '_', '_', '_', '_'], ['_', '_', 'O', '_', '_', '_']]"""
        # size = 7
        """self.board = [['X', 'X', 'X', 'X', 'X', 'O', 'O'], ['X', 'X', 'X', 'X', 'X', 'O', 'O'],
                      ['X', 'X', 'X', 'X', 'O', 'O', 'O'], ['_', '_', '_', 'O', '_', 'O', 'O'],
                      ['_', '_', 'O', '_', '_', 'O', 'O'], ['_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', 'O', 'O', '_', '_']]"""

    # checking if move is valid
    def check_move(self, move):
        if move is None:
            return False
        elif self.board[move[0]][move[1]] == "_":
            self.board[move[0]][move[1]] = self.symbol
            return True
        elif self.board[move[0]][move[1]] in ("X", "O"):
            return False
        else:
            return False

    # checking if sb won the game
    def check_win(self):
        # check if sb win and check if there are any empty fields left
        # If there aren't any empty fields - draw_f = True
        def check_horizontal():
            win = None
            draw_f = True
            for index, cell_row in enumerate(self.board):
                if all(x == cell_row[0] for x in cell_row) and cell_row[0] != "_":
                    win = cell_row[0]
                    self.win_coordinates = [0, index]
                if any(x == "_" for x in cell_row):
                    draw_f = False
            """if win:
                return win, None
            elif draw_f:
                return None, draw_f
            else:
                return win, None"""
            return win, draw_f

        def check_vertical():
            win = None
            for y in range(len(self.board)):
                for x in range(1, len(self.board)):
                    if self.board[x - 1][y] == self.board[x][y] and self.board[x][y] != "_":
                        win = self.board[x][y]
                        self.win_coordinates = [1, y]
                    else:
                        win = None
                        self.win_coordinates = [None, None]
                        break

                if win:
                    break
            return win

        def check_crossing():
            win = None
            x = 1
            y = 1

            while x < len(self.board):

                if self.board[x][y] == self.board[x - 1][y - 1] and self.board[x][y] != "_":
                    win = self.board[x][y]
                    self.win_coordinates = [2, 0]
                else:
                    win = None
                    self.win_coordinates = [None, None]
                    break
                x += 1
                y += 1

            if not win:
                x = len(self.board) - 2
                y = 1

                while x >= 0:
                    if self.board[x][y] == self.board[x + 1][y - 1] and self.board[x][y] != "_":
                        win = self.board[x][y]
                        self.win_coordinates = [3, 0]
                    else:
                        win = None
                        self.win_coordinates = [None, None]
                        break

                    x -= 1
                    y += 1
            return win

        winner, draw = check_horizontal()
        if not winner:
            winner = check_vertical()
        if not winner:
            winner = check_crossing()

        # if self.win and self.win != "_":
        if winner:
            self.game_status = winner
        elif draw:
            self.game_status = "_"

    # easy difficulty - all random moves
    def easy_mode(self):
        logging.debug('Making move level "easy"')
        while True:
            computer_move = [
                random.randint(0, len(self.board) - 1),
                random.randint(0, len(self.board) - 1),
            ]
            if self.check_move(computer_move):
                break

    # medium difficulty - random moves until somebody can win. If there is situation that computer can win or block
    # the enemy it will go for the win
    def medium_mode(self):
        logging.debug('Making move level "medium"')

        def check_horizontal_medium():
            computer_move_function = None
            for index, cell_row in enumerate(self.board):
                # if amount of "X" is one less than size and there is empty field in row
                if cell_row.count("X") == self.size - 1 and any(x == "_" for x in cell_row):
                    computer_move_function = [index, cell_row.index("_")]
                    # if symbol is the same as "X" break - will go for then win
                    if self.symbol == "X":
                        break
                # same as above
                elif cell_row.count("O") == self.size - 1 and any(
                        x == "_" for x in cell_row
                ):
                    computer_move_function = [index, cell_row.index("_")]
                    if self.symbol == "O":
                        break
            return computer_move_function

        def check_vertical_medium():

            computer_move_function = None
            computer_move_previous = None

            for y in range(len(self.board)):
                # amount of "X" and "O" in column
                number_x = 0
                number_o = 0
                for x in range(len(self.board)):
                    if self.board[x][y] == "_":
                        computer_move_function = (x, y)
                    elif self.board[x][y] == "O":
                        number_o += 1
                    elif self.board[x][y] == "X":
                        number_x += 1
                # if there are size - 1 signs and empty space was found
                if number_o == self.size - 1 and computer_move_function:
                    # if symbol is equal to "O" - instant win:
                    computer_move_previous = computer_move_function
                    if self.symbol == "O":
                        return computer_move_function
                elif number_x == self.size - 1 and computer_move_function:
                    computer_move_previous = computer_move_function
                    if self.symbol == "X":
                        return computer_move_function
                    """if (number_o == self.size - 1 or number_x == self.size - 1) and computer_move_function:
                    print(computer_move_previous)
                    computer_move_previous = computer_move_function"""
                else:
                    computer_move_function = None
            logging.debug(f"Returning computer previous: {computer_move_previous}")
            return computer_move_previous

        def check_crossing_medium():
            x = 0
            y = 0
            computer_move_function = None
            number_x = 0
            number_o = 0
            while x < len(self.board):
                if self.board[x][y] == "_":
                    computer_move_function = (x, y)
                elif self.board[x][y] == "O":
                    number_o += 1
                elif self.board[x][y] == "X":
                    number_x += 1
                x += 1
                y += 1

            if number_x == self.size - 1 and computer_move_function and self.symbol == "X":
                return computer_move_function
            elif number_o == self.size - 1 and computer_move_function and self.symbol == "O":
                return computer_move_function
            if number_x == self.size - 1 or number_o == self.size - 1 and computer_move_function:
                pass
            else:
                computer_move_function = None
            if computer_move_function is None:
                x = len(self.board) - 1
                y = 0
                number_x = 0
                number_o = 0
                # computer_move_2 = None
                while x >= 0:
                    if self.board[x][y] == "_":
                        computer_move_function = (x, y)
                    elif self.board[x][y] == "O":
                        number_o += 1
                    elif self.board[x][y] == "X":
                        number_x += 1
                    x -= 1
                    y += 1

            if number_x == self.size - 1 and computer_move_function and self.symbol == "X":
                return computer_move_function
            elif number_o == self.size - 1 and computer_move_function and self.symbol == "O":
                return computer_move_function
            if number_x == self.size - 1 or number_o == self.size - 1 and computer_move_function:
                pass
            else:
                computer_move_function = None

            return computer_move_function

        computer_move = check_horizontal_medium()
        logging.debug(f"computer move medium_horizontal: {computer_move}")
        temporary = check_vertical_medium()
        if temporary:
            computer_move = temporary
        temporary_2 = check_crossing_medium()
        if temporary_2:
            computer_move = temporary_2
        # logging.debug(f"computer move before loop: {computer_move}")
        self.check_move(computer_move)
        if computer_move is None:
            while True:
                # logging.debug("IN LOOP")
                computer_move = [
                    random.randint(0, len(self.board)) - 1,
                    random.randint(0, len(self.board) - 1),
                ]
                if self.check_move(computer_move):
                    break

    # special function to check winner but specified for minimax
    def check_win_minimax(self):
        def check_horizontal():
            winner_f = None
            draw_f = True
            for index, cell_row in enumerate(self.board):
                if all(x == cell_row[0] for x in cell_row) and cell_row[0] != "_":
                    winner_f = cell_row[0]
                if any(x == "_" for x in cell_row):
                    draw_f = False

            if winner_f:
                return winner_f
            elif draw_f:
                return "."
            else:
                return winner_f

        def check_vertical():
            winner_f = None
            for y in range(len(self.board)):
                for x in range(len(self.board)):
                    if self.board[x][y] == "_":
                        winner_f = None
                        break
                    elif self.board[x - 1][y] == self.board[x][y]:
                        winner_f = self.board[x][y]
                    else:
                        winner_f = None
                        break

                if winner_f:
                    break
            return winner_f

        def check_crossing():
            winner_f = None
            # print("checking crossing...")
            x = 0
            y = 0

            while x < len(self.board):
                if self.board[x][y] == "_":
                    winner_f = None
                    break
                elif x == 0:
                    pass
                elif self.board[x][y] == self.board[x - 1][y - 1]:
                    winner_f = self.board[x][y]
                else:
                    winner_f = None
                    break
                x += 1
                y += 1

            if not winner_f:
                x = len(self.board) - 1
                y = 0

                while x >= 0:
                    # while y < len(board):
                    if self.board[x][y] == "_":
                        winner_f = None
                        break
                    elif y == 0:
                        pass
                    elif self.board[x][y] == self.board[x + 1][y - 1]:
                        winner_f = self.board[x][y]
                    else:
                        winner_f = None
                        break

                    x -= 1
                    y += 1
            return winner_f

        # logging.debug(self.board)
        winner = check_vertical()
        # logging.debug(f"winner after horizontal: {winner}")
        if winner:
            return winner
        winner = check_crossing()
        # logging.debug(f"winner after vertical: {winner}")
        if winner:
            return winner
        winner = check_horizontal()
        return winner

        # logging.debug(f"winner after crossing: {winner}")

    def hard_mode(self):
        # time.sleep(1)
        logging.debug('Making move level "hard 4"')
        start_f = time.time()

        move = self.minimax(True, -20, 20, None, 0)

        end_f = time.time()

        logging.debug(f"HARD MOVE TIME: {end_f - start_f}")
        logging.debug(f"Hard moves amount: {self.hard_moves_amount}")
        logging.debug(f"Max depth: {self.max_depth}")
        # for testing
        self.hard_moves_amount = 0
        self.max_depth = 0
        # making move - hard
        self.check_move(move[1])

    # minimax algorithm for hard difficulty
    def minimax(self, maximizing, alpha, beta, move, depth):
        # for testing
        self.hard_moves_amount += 1
        if depth > self.max_depth:
            self.max_depth = depth

        scores = {"win": 10, "lost": -10, "draw": 0}
        winner = self.check_win_minimax()

        if winner:
            if self.symbol == winner:
                return [scores["win"], move]
            elif winner == ".":
                return [scores["draw"], move]
            else:
                return [scores["lost"], move]
        max_depth = 8
        if self.size > 4:
            max_depth = 7
        if depth > max_depth:
            return [scores["draw"], move]

        # maximizing move (finding AI best move)
        if maximizing:
            best_score = -20
            move = None
            for x in range(len(self.board)):
                for y in range(len(self.board)):
                    if self.board[x][y] == "_":
                        self.board[x][y] = self.symbol

                        score = self.minimax(False, alpha, beta, move, depth + 1)
                        if score[0] > best_score:
                            best_score = score[0]
                            move = [x, y]

                        self.board[x][y] = "_"
                        if best_score >= beta:
                            return [best_score, move]
                        if best_score > alpha:
                            alpha = best_score

            return [best_score, move]
        # minimizing - (finding enemy best move)
        else:
            best_score = 20
            move = None
            for x in range(len(self.board)):
                for y in range(len(self.board)):
                    if self.board[x][y] == "_":
                        if self.symbol == "X":
                            temporary_symbol = "O"
                        else:
                            temporary_symbol = "X"
                        self.board[x][y] = temporary_symbol

                        score = self.minimax(True, alpha, beta, move, depth + 1)

                        if score[0] < best_score:
                            best_score = score[0]
                            move = [x, y]

                        self.board[x][y] = "_"

                        if best_score <= alpha:
                            return [best_score, move]
                        if best_score < beta:
                            beta = best_score
            return [best_score, move]

    # function to reverse symbol
    def reverse_symbol(self):
        if self.symbol == "O":
            self.symbol = "X"
        else:
            self.symbol = "O"
