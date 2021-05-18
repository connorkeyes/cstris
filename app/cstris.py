# references:
# https://realpython.com/python3-object-oriented-programming/ used to learn about python OOP
# https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318 used and modified this example for core tetris app


import pygame
import random
import time

colors = [
    (0, 0, 0), # placeholder; colors[0] not used
    (0, 255, 255), # Aqua (line piece)
    (255, 69, 0), # Red (z piece)
    (0, 205, 102), # Green (s piece)
    (58, 95, 205), # Royal Blue (reverse L piece)
    (255, 128, 0), # Orange (L piece)
    (255, 131, 250), # Purple (T piece)
    (255, 255, 0), # Yellow (square piece)
]


class Figure:
    """
    This class holds all of the figures or "tetris shapes" that the game will randomly choose.
    Member Variable: Figures (shape of every figure on a 4x4 grid)
    Member Functions: __init__ (initialize a figure), image (return image of chosen figure),
        rotation functions (rotate a figure)
    """

    # init x and y to zero
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], # line piece
        [[4, 5, 9, 10], [2, 6, 5, 9]], # z piece
        [[6, 7, 9, 10], [1, 5, 6, 10]], # s piece
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # reverse L piece
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L piece
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # T piece
        [[1, 2, 5, 6]], # square piece
    ]

    def __init__(self, x, y):
        """
        Initializes a figure.
        Params: self, x, y
        """

        # init x and y
        self.x = x
        self.y = y

        # choose a random int between 0 and length of figures list - 1
        self.type = random.randint(0, len(self.figures) - 1)

        # set color to same int as type to make color the same for the same figure
        self.color = self.type + 1

        # init rotation to 0
        self.rotation = 0

    def image(self):
        """
        Returns the proper rotation of the chosen type of figure.
        Params: self
        """
        return self.figures[self.type][self.rotation]

    def rotateLeft(self):
        """
        Rotates the figure left 90 degrees by finding the modulus of the rotation int and
        the amount of rotation figures that exist for the respective type of figure.
        """
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
    
    def rotateRight(self):
        """
        Rotates the figure right 90 degrees by finding the modulus of the rotation int - 1 and
        the amount of rotation figures that exist for the respective type of figure.
        """

        # if rotation = 0, use last rotation figure on the figure list; else, subtract 1 from rotation
        # (avoids error by disallowing rotation from becoming negative)
        if self.rotation == 0:
            self.rotation = len(self.figures[self.type]) - 1
        else:
            self.rotation = (self.rotation - 1) % len(self.figures[self.type])

    def rotate180(self):
        """
        Rotates the figure 180 degrees by finding the modulus of the rotation int + 2 and
        the amount of rotation figures that exist for the respective type of figure.
        """
        self.rotation = (self.rotation + 2) % len(self.figures[self.type])


class Tetris:
    """
    This class holds all the variables of the tetris game.
    Member Variable: Figures (shape of every figure on a 4x4 grid)
    Member Functions: __init__ (initializes the game), new_figure (creates new figure)
    """
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    lines_left = 0
    start_time = 0
    timer = 0
    final_time = 0

    def __init__(self, height, width, lines_left):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.lines_left = lines_left
        self.start_time = time.time()
        self.timer = 0
        self.final_time = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        """
        Creates new figure object at x=3, y=0
        Params: self
        """
        self.figure = Figure(3, 0)

    def intersects(self):
        """
        Returns whether or not a newly created figure is outside the bounds of the game.
        If a newly created figure is intersecting, game over.
        Params: self
        """
        intersection = False

        # loop through every block in the 4x4 matrix, i*4+j covers every number from 0-15
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.lines_left -= lines
        if self.lines_left <= 0:
            self.state = "gameover"

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self, direction):
        old_rotation = self.figure.rotation
        if direction == "left":
            self.figure.rotateLeft()
        elif direction == "right":
            self.figure.rotateRight()
        elif direction == "180":
            self.figure.rotate180()
        
        if self.intersects():
            self.figure.rotation = old_rotation


# Initialize the game engine
pygame.init()

# Initialize counter to stop the loop when the game ends
stop_loop_count = 0

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Cstris")

# Loop until the user clicks the close button or the game ends.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10, 40)
counter = 0

pressing_down = False

start_time = time.time()
final_time = time.time()

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 0.5
    if counter > 100000:
        counter = 0

    if fps != 0:
        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate("right")
            if event.key == pygame.K_z:
                game.rotate("left")
            if event.key == pygame.K_a:
                game.rotate("180")
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10, 1)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    game.timer = round(time.time() - start_time, 2)

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    lines_left_cap = font.render("Lines Left: ", True, BLACK)
    lines_left_num = font.render(str(game.lines_left), 25, colors[2])
    timer_cap = font.render("Time: " + str(game.timer) + "s", True, BLACK)
    text_game_over = font1.render("Game Over!", True, BLACK)
    text_final_time = font1.render("Time: " + str(round(final_time, 2)), True, colors[2])

    screen.blit(lines_left_cap, [130, 15])
    screen.blit(lines_left_num, [260, 15])
    if game.state == "start":
        screen.blit(timer_cap, [130, 470])
    if game.state == "gameover":
        stop_loop_count += 1
        if stop_loop_count == 1:
            final_time = time.time() - start_time
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_final_time, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

print(final_time)