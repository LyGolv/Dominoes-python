import random
import time


class Dominoes:
    def __init__(self):
        self.dominoes_pieces = [[i, j] for i in range(7) for j in range(i, 7)]
        player_pieces, computer_pieces, self.dominoes_pieces = self.distribute_pieces()
        self.player = Player("player", player_pieces)
        self.computer = Player("computer", computer_pieces)
        self.domino_snake = []
        self.status = ""
        self.update_status_and_snake()

    def text(self):
        return {
            self.player.name: "It's your turn to make a move. Enter your command.",
            self.computer.name: "Computer is about to make a move. Press Enter to continue...",
            "win_p": "The game is over. You won!",
            "win_c": "The game is over. The computer won!",
            "win_o": "The game is over. It's a draw!"
        }[self.status]

    def start(self):
        while True:
            print("======================================================================")
            print("Stock size:", len(self.dominoes_pieces))
            print("Computer pieces:", len(self.computer.pieces))
            self.display_snake()
            print("\n\nYour pieces:")
            self.player.display_pieces()
            self.status = self.find_winner()
            print("\nStatus:", self.text())
            if self.status in ["win_p", "win_c", "win_o"]:
                break
            choice = self.computer_move() if self.status == self.computer.name else self.player_move()
            self.make_move(choice, self.player.pieces if self.status == self.player.name else self.computer.pieces)
            self.status, *_ = {self.player.name, self.computer.name} - {self.status}

    def generate_possibilities(self):
        num = ''.join(map(lambda x: f"{x[0]}{x[1]}", self.domino_snake)) + ''.join(
            map(lambda x: f"{x[0]}{x[1]}", self.computer.pieces))
        d = {}
        for piece in self.computer.pieces:
            val = num.count(f"{piece[0]}") + num.count(f"{piece[1]}")
            if val not in d:
                d[val] = [piece]
            else:
                d[val].append(piece)
        return [piece for i in sorted(d.keys(), reverse=True) for piece in d[i]]

    def computer_move(self):
        input()
        for domino in self.generate_possibilities():
            i = self.computer.pieces.index(domino)
            if self.is_good_move(self.computer.pieces, i + 1):
                return i + 1
        return 0

    def player_move(self):
        while True:
            choice = input()
            if not choice.replace('-', '', 1).isdigit() or not -len(self.player.pieces) <= int(
                    choice) <= len(self.player.pieces):
                print("Invalid input. Please try again.")
            elif not self.is_good_move(self.player.pieces, int(choice)):
                print("Illegal move. Please try again.")
            else:
                return int(choice)

    def is_good_move(self, current_player_pieces, choice):
        if choice == 0:
            return True
        elif choice < 0:
            if current_player_pieces[abs(choice) - 1][0] == self.domino_snake[0][0] \
                    or current_player_pieces[abs(choice) - 1][1] == self.domino_snake[0][0]:
                return True
        elif choice > 0:
            if current_player_pieces[abs(choice) - 1][0] == self.domino_snake[-1][1] \
                    or current_player_pieces[abs(choice) - 1][1] == self.domino_snake[-1][1]:
                return True
        return False

    def distribute_pieces(self):
        random.shuffle(self.dominoes_pieces)
        while not Player.contains_double_domino(self.dominoes_pieces[:7]) and not Player.contains_double_domino(
                self.dominoes_pieces[7:14]):
            random.shuffle(self.dominoes_pieces)
        return self.dominoes_pieces[:7], self.dominoes_pieces[7:14], self.dominoes_pieces[14:]

    def update_status_and_snake(self):
        player_max_double_dominoes = max(list(filter(lambda x: x[0] == x[1], self.player.pieces)) + [[0, 0]])
        computer_max_double_dominoes = max(list(filter(lambda x: x[0] == x[1], self.computer.pieces)) + [[0, 0]])
        self.domino_snake.append(max(player_max_double_dominoes, computer_max_double_dominoes))
        if player_max_double_dominoes[0] >= computer_max_double_dominoes[0]:
            self.player.pieces.remove(player_max_double_dominoes)
            self.status = self.computer.name
        else:
            self.computer.pieces.remove(computer_max_double_dominoes)
            self.status = self.player.name

    def display_snake(self):
        if len(self.domino_snake) < 7:
            print(f"\n{''.join(map(str, self.domino_snake))}")
        else:
            print(f"\n{''.join(map(str, self.domino_snake[:3]))}...{''.join(map(str, self.domino_snake[-3:]))}")

    def find_winner(self):
        win = self.status
        if len(self.player.pieces) == 0:
            win = "win_p"
        elif len(self.computer.pieces) == 0:
            win = "win_c"
        elif ''.join(map(str, self.domino_snake)).count(f"{self.domino_snake[-1][1]}") >= 8 \
                or ''.join(map(str, self.domino_snake)).count(f"{self.domino_snake[0][0]}") >= 8:
            win = "win_o"
        return win

    def make_move(self, choice, current_player_pieces):
        if choice == 0:
            if self.dominoes_pieces:
                current_player_pieces += [self.dominoes_pieces.pop(0)]
        elif choice < 0:
            domino = current_player_pieces.pop(abs(choice) - 1)
            domino = domino if domino[1] == self.domino_snake[0][0] else domino[::-1]
            self.domino_snake.insert(0, domino)
        else:
            domino = current_player_pieces.pop(choice - 1)
            domino = domino if domino[0] == self.domino_snake[-1][1] else domino[::-1]
            self.domino_snake.append(domino)


class Player:
    def __init__(self, name, pieces=None):
        self.name = name
        self.pieces = [] if pieces is None else pieces

    def display_pieces(self):
        for i, piece in enumerate(self.pieces):
            print(f"{i + 1}:{piece}")

    @staticmethod
    def contains_double_domino(piece_set):
        return any(piece[0] == piece[1] for piece in piece_set)


def main():
    random.seed(time.time())
    dominoes = Dominoes()
    dominoes.start()


if __name__ == "__main__":
    main()
