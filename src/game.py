import texttable as tt
import random


class Game:
    def __init__(self):
        self.width = None
        self.height = None
        self.num_apples = None
        self.load_settings()
        self.snake = [(3, 2), (3, 3), (3, 4)]
        self.apples = []
        self.direction = 'U'  # We presume that the snake's initial direction is UP
        self.game_over = False
        self.place_apples()

    def load_settings(self):
        with open('settings.properties', 'r') as file:
            settings = {}
            for line in file:
                key, value = line.strip().split('=')
                settings[key] = int(value)
            self.width = settings.get('N', 7)
            self.height = settings.get('N', 7)
            self.num_apples = settings.get('num_apples', 10)

    @staticmethod
    def is_adjacent(pos1, pos2):
        """
        Check if 2 apples are adjacent
        :param pos1: position of the first apple
        :param pos2: position of the second apple
        :return: True or False
        """
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

    def place_apples(self):
        """
        Place the apples on the board in a convenient way -> no adjacent apples
        :return:
        """
        while len(self.apples) < self.num_apples:
            new_apples = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if all(not self.is_adjacent(new_apples, f) for f in self.apples) and new_apples not in self.snake:
                self.apples.append(new_apples)

    def create_board(self):
        table = tt.Texttable()
        """
        x and y are the index coordinates to move through the board
        """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    row.append('*')  # Representing the head of the snake
                elif (x, y) in self.snake:
                    row.append('+')  # Representing the body of the snake
                elif (x, y) in self.apples:
                    row.append('a')  # Representing the apples
                else:
                    row.append(' ')
            table.add_row(row)
        return table.draw()

    def update_snake(self, steps=1):
        """

        :param steps: number of squares the snake will move to
        :return: None
        head_x and head_y - coordinates of the snake's head
        """
        for _ in range(steps):
            head_x, head_y = self.snake[0]
            if self.direction == 'U':
                head_y -= 1
            elif self.direction == 'D':
                head_y += 1
            elif self.direction == 'L':
                head_x -= 1
            elif self.direction == 'R':
                head_x += 1
            new_head = (head_x, head_y)
            self.snake.insert(0, new_head)

            # Check if the snake hits the edge of the game area or one of its own segments
            if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height or self.snake[0] in self.snake[1:]:
                self.game_over = True
                return

            if new_head in self.apples:
                self.apples.remove(new_head)
                # self.place_apples()
            else:
                self.snake.pop()

    @staticmethod
    def is_opposite_direction(current, new):
        opposites = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
        return opposites.get(current) == new


class UI:
    def __init__(self):
        self.game = Game()

    def run(self):
        while not self.game.game_over:
            print(self.game.create_board())
            command = input("Enter command (right, up, left, down, move[n]): ").lower()

            if command in ['right', 'up', 'left', 'down']:
                new_direction = command[0].upper()
                if self.game.is_opposite_direction(self.game.direction, new_direction):
                    print("Error: Cannot reverse direction directly!")
                    continue
                else:
                    self.game.direction = new_direction
            elif command.startswith("move"):
                steps = command[4:]
                steps = 1 if steps == '' else int(steps)
                self.game.update_snake(steps)
                continue

            self.game.update_snake()

            if self.game.game_over:
                print("Game Over!")

