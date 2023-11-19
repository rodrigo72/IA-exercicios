
class Board:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.player = 'O'
        self.bot = 'X'

    def __str__(self):
        board_str = self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2] + '\n'
        board_str += "--+---+--\n"
        board_str += self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5] + '\n'
        board_str += "--+---+--\n"
        board_str += self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8] + '\n'
        return board_str

    def space_is_free(self, index):
        return self.board[index] == ' '

    def insert(self, pos, player):
        if self.space_is_free(pos):
            self.board[pos] = player
            if self.check_draw():
                print("Draw!")
                return True
            winner = self.check_win()
            if winner is not None:
                print(winner + " wins!")
                return True
        return False

    def check_draw(self):
        return ' ' not in self.board

    def check_win(self):
        # horizontal
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != ' ':
                return self.board[i]

        # vertical
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                return self.board[i]

        # diagonal
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return self.board[2]

        return None

    def player_move(self):
        while True:
            pos = int(input("Enter position for " + self.player + ": "))
            if 0 <= pos < 9 and self.space_is_free(pos):
                return self.insert(pos, self.player)
            else:
                print("Invalid move. Try again.")

    def get_available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def bot_move(self):
        best_score = -1000
        best_move = 0

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.bot
                # score = self.minimax(10, False)
                score = self.minimax_2(10, -1000, 1000, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i

        return self.insert(best_move, self.bot)

    def minimax(self, depth, is_maximizing):
        result = self.check_win()
        if result == self.bot:
            return 1
        if result == self.player:
            return -1
        if self.check_draw():
            return 0
        if depth == 0:
            return 0

        if is_maximizing:
            best_score = -1000  # -inf
            for move in self.get_available_moves():
                self.board[move] = self.bot
                best_score = max(best_score,
                                 self.minimax(depth - 1, False))
                self.board[move] = ' '
            return best_score
        else:
            best_score = 1000  # +inf
            for move in self.get_available_moves():
                self.board[move] = self.player
                best_score = min(best_score,
                                 self.minimax(depth - 1, True))
                self.board[move] = ' '
            return best_score

    def minimax_2(self, depth, alpha, beta, is_maximizing):
        result = self.check_win()
        if result == self.bot:
            return 1
        if result == self.player:
            return -1
        if self.check_draw() or depth == 0:
            return 0

        if is_maximizing:
            max_score = -1000  # -inf
            for move in self.get_available_moves():
                self.board[move] = self.bot
                score = self.minimax_2(depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                self.board[move] = ' '
                alpha = max(alpha, score)
                if beta <= alpha:
                    break

            return max_score
        else:
            min_score = 1000  # +inf
            for move in self.get_available_moves():
                self.board[move] = self.player
                score = self.minimax_2(depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                self.board[move] = ' '
                beta = min(beta, score)
                if beta <= alpha:
                    break

            return min_score


if __name__ == "__main__":
    board = Board()
    done = False
    while not done:
        print(board)
        done = board.player_move()
        if done:
            break
        print(board)
        done = board.bot_move()
    print(board)
