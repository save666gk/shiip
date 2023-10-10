import random
import itertools

board_size = [6, 6]
ordered_ships = []


class SeaBattleError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'SeaBattleError -> {0} '.format(self.message)
        else:
            return 'SeaBattleError has been raised'


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:

    def __init__(self, length, nose, orientation):
        self.ship_dots = []
        self.length = length
        self.nose = nose
        self.orientation = orientation
        self.hit_points = length

    def dots(self):
        for i in range(self.length):
            if self.orientation == 'v':
                self.ship_dots.append(Dot(self.nose[0] + i, self.nose[1]))
        for i in range(self.length):
            if self.orientation == 'h':
                self.ship_dots.append(Dot(self.nose[0], self.nose[1] + i))
        return self.ship_dots


class Board:

    ship_list = []
    ships_afloat = 0
    board_dots = []

    def add_ship(self, length):
        for i in range(50):
            x = random.randrange(board_size[0])
            y = random.randrange(board_size[1])
            nose = [x, y]
            orientation = random.choice(["v", "h"])
            ship = Ship(length, nose, orientation)
            ship.ship_dots = ship.dots()
            if self.out(ship.ship_dots[-1]):
                continue
            space_occupied = False
            for ship_deck in ship.ship_dots:
                if self.board_dots[ship_deck.x][ship_deck.y] != '.':
                    space_occupied = True
                    break
            if space_occupied:
                continue
            for ship_deck in ship.ship_dots:
                self.board_dots[ship_deck.x][ship_deck.y] = 'o'
            self.ship_list.append(ship)
            self.ships_afloat = self.ships_afloat + 1
            return True
        return False

    def contour(self):
        for a, b in itertools.product(range(board_size[0]), range(board_size[1])):
            if self.board_dots[a][b] != 'o':
                continue
            x = a - 1
            y = b - 1
            for i in range(3):
                if x < 0 or x >= board_size[0]:
                    x += 1
                    continue
                for j in range(3):
                    if y < 0 or y >= board_size[1]:
                        y += 1
                        continue
                    if self.board_dots[x][y] == '.':
                        self.board_dots[x][y] = '-'
                    y += 1
                x += 1
                y = b - 1

    def out(self, dot):
        if dot.x >= board_size[0] or dot.y >= board_size[1] or dot.x < 0 or dot.y < 0:
            return True
        return False

    def shot(self, x, y):
        hit_dot = Dot(x, y)
        if self.out(hit_dot):
            raise SeaBattleError('Beyond the game field borders')
        if self.board_dots[x][y] == 'x' or self.board_dots[x][y] == 'X':
            raise SeaBattleError('This dot is already shot')
        elif self.board_dots[x][y] == '.' or self.board_dots[x][y] == '-':
            self.board_dots[x][y] = 'x'
            return False
        else:
            self.board_dots[x][y] = 'X'
            for a_ship in self.ship_list:
                if hit_dot in a_ship.ship_dots:
                    a_ship.hit_points = a_ship.hit_points - 1
                    print('\nShip hit...')
                    if a_ship.hit_points == 0:
                        print('\nShip sunk...')
                        self.ships_afloat = self.ships_afloat - 1
            return True


class Player:

    human_board = Board()
    machine_board = Board()

    def ask(self):
        pass

    def move(self, enemy_board):
        while True:
            hit_dot = self.ask()
            try:
                if enemy_board.shot(hit_dot.x, hit_dot.y):
                    return True
            except SeaBattleError as error:
                print(error)
                continue
            return False


class Ai(Player):

    def ask(self):
        for a, b in itertools.product(range(board_size[0]), range(board_size[1])):
            if self.human_board.board_dots[a][b] != 'X':
                continue
            if b + 1 < board_size[1]:
                if (self.human_board.board_dots[a][b + 1] != 'x' and
                        self.human_board.board_dots[a][b + 1] != 'X'):
                    return Dot(a, b + 1)
            if a + 1 < board_size[0]:
                if (self.human_board.board_dots[a + 1][b] != 'x' and
                        self.human_board.board_dots[a + 1][b] != 'X'):
                    return Dot(a + 1, b)
            if b - 1 > 0:
                if (self.human_board.board_dots[a][b - 1] != 'x' and
                        self.human_board.board_dots[a][b - 1] != 'X'):
                    return Dot(a, b - 1)
            if a - 1 > 0:
                if (self.human_board.board_dots[a - 1][b] != 'x' and
                        self.human_board.board_dots[a - 1][b] != 'X'):
                    return Dot(a - 1, b)
        while True:
            x = random.randrange(board_size[0])
            y = random.randrange(board_size[1])
            if self.human_board.board_dots[x][y] != 'x' and self.human_board.board_dots[x][y] != 'X':
                return Dot(x, y)


class User(Player):

    def ask(self):
        while True:
            try:
                c, r, *a = map(int, input('\n Make your move (column row): ').split())
            except ValueError:
                print('Enter two integers please!')
                continue
            return Dot(r, c)


class Game:

    human = User()
    human_board = human.human_board
    machine = Ai()
    machine_board = machine.machine_board

    def random_board(self, board):
        for i in range(100):
            board.board_dots = [['.'] * board_size[1] for i in range(board_size[0])]
            board.ships_afloat = 0
            board.ship_list = []
            for j in ordered_ships:
                if board.add_ship(j):
                    board.contour()
                    continue
                else:
                    break
            if board.ships_afloat == len(ordered_ships):
                return True
        return False

    def show_boards(self):
        first_line = []
        interval1 = ' ' * 15
        interval2 = ' ' * (25 - 2 * board_size[1])

        for i in range(board_size[1]):
            first_line.append(str(i))
        first_line = ' '.join(first_line)
        print(f'\n  Human board {interval1} Machine board')
        print(f'\n  {first_line} {interval2}   {first_line}')
        for i in range(board_size[0]):
            row1 = ' '.join(self.human_board.board_dots[i])
            row1 = row1.replace('-', '.')
            row2 = ' '.join(self.machine_board.board_dots[i])
            row2 = row2.replace('-', '.')
            row2 = row2.replace('o', '.')
            print(f'{i} {row1} {interval2} {i} {row2}')

    def loop(self):
        if not self.random_board(self.human_board) or not self.random_board(self.machine_board):
            print('\nToo many ships ordered.')
            return
        while True:
            self.show_boards()
            while self.human.move(self.machine_board):
                if self.machine_board.ships_afloat == 0:
                    self.show_boards()
                    print('\nCongratulations, human won!')
                    return
                self.show_boards()
            while self.machine.move(self.human_board):
                if self.human_board.ships_afloat == 0:
                    print('\nCongratulations, machine won!')
                    return

    def greet(self):
        print('\n   Sea battle game!')
        try:
            board_size[1], board_size[0], *a = (
                map(int, input('\nВыберите размер доски (ширина и высота, от 3 до 10, по умолчанию 6x6): ').split()))
        except ValueError:
            pass
        n = input('Количество трехпалубных кораблей (по умолчанию 1): ')
        if not n.isdigit() or int(n) < 0 or int(n) > 3:
            n = 1
        for i in range(int(n)):
            ordered_ships.append(3)
        n = input('Количество двухпалубных кораблей (по умолчанию 2): ')
        if not n.isdigit() or int(n) < 0 or int(n) > 5:
            n = 2
        for i in range(int(n)):
            ordered_ships.append(2)
        n = input('Количество однопалубных кораблей (по умолчанию 4): ')
        if not n.isdigit() or int(n) < 0 or int(n) > 7:
            n = 4
        for i in range(int(n)):
            ordered_ships.append(1)


party = Game()
party.greet()
party.loop()