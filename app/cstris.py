# references:
# https://realpython.com/python3-object-oriented-programming/ used to learn about python OOP
# https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318 used and modified this example for core tetris app
# https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python used for generating code


import pygame
import random
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
import string

load_dotenv()

# initialize set of colors that associate with each piece
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

def start_game(gamemode, challenger, challenger_time, challenge_mode):

    gamemodes = [10, 20, 40]

    # Initialize the game engine and music engine
    pygame.init()
    pygame.mixer.init()

    # load music and sound effect to play when lines are cleared
    rootDir = os.path.dirname(os.path.abspath("top_level_file.txt"))
    music = os.path.join(rootDir + "/sounds/music.mp3")
    sound_effect = os.path.join(rootDir + "/sounds/clear.wav")


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
    game = Tetris(20, 10, gamemodes[gamemode - 1])
    counter = 0

    # play music
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

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
        text_you_win = font1.render("You Win!", True, colors[3])
        text_you_lose = font1.render("You Lose!", True, colors[2])
        text_challenger_time = font.render(challenger + " Time: " + str(challenger_time), True, BLACK)
       


        screen.blit(lines_left_cap, [130, 15])
        screen.blit(lines_left_num, [260, 15])
        if game.state == "start":
            screen.blit(timer_cap, [130, 470])

        if challenge_mode == False:
            if game.state == "gameover":
                stop_loop_count += 1
                if stop_loop_count == 1:
                    final_time = time.time() - start_time
                    pygame.mixer.music.stop()
                screen.blit(text_game_over, [20, 200])
                screen.blit(text_final_time, [25, 265])
        else:
            if game.state == "gameover":
                stop_loop_count += 1
                if stop_loop_count == 1:
                    final_time = time.time() - start_time
                    pygame.mixer.music.stop()
                if final_time <= float(challenger_time):
                    screen.blit(text_you_win, [20, 200])
                    screen.blit(text_final_time, [20, 265])
                    screen.blit(text_challenger_time, [20, 330])
                else:
                    screen.blit(text_you_lose, [20, 200])
                    screen.blit(text_final_time, [20, 265])
                    screen.blit(text_challenger_time, [20, 330])

        pygame.display.flip()
        clock.tick(fps)

        # pygame.quit()
    
    return final_time

def display_menu():
    choices = [1,2,3,4]
    choice = 0
    while choice not in choices:
        print("***********************************")
        print("Please select an option from the menu below: ")
        print("Play Solo - 1")
        print("Send Challenge - 2")
        print("Receive Challenge - 3")
        print("Exit - 4")
        choice = int(input("***********************************\n"))
        if choice not in choices:
            print("Please select a valid choice.\n")
            continue
        return choice

def display_gamemodes():
    choices = [1,2,3,4]
    choice = 0
    while choice not in choices:
        print("***********************************")
        print("10 Lines - 1")
        print("20 Lines - 2")
        print("40 Lines - 3")
        choice = int(input("***********************************\n"))
        if choice not in choices:
            print("Please select a valid choice.\n")
            continue
        return choice

def generate_code(name, final_time, gamemode):
    nums = string.digits
    code = ''.join(random.choice(nums) for i in range(50))
    final_time_str = str(round(final_time, 2))
    code = name + code[:25] + final_time_str + code[25:] + str(gamemode)                
    return code


def send_challenge(username, email, final_time, gamemode):
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")
    client = SendGridAPIClient(SENDGRID_API_KEY)
    subject = username + " has challenged you to Cstris!"
    code = generate_code(username, final_time, gamemode)
    html_content = f"""
    <h3> You've been challenged to Cstris by {username}! </h3>
    <ol>
        Challenge Code: {code}
    </ol>
    <ol>
        Paste the above code into your Cstris and show {username} who's boss!
    </ol>
    <ol>
        (Don't have Cstris? Get it here: https://github.com/connorkeyes/cstris)
    </ol>
    """

    message = Mail(from_email=SENDER_ADDRESS, to_emails=email, subject=subject, html_content=html_content)

    try:
        response = client.send(message)
        print("Your challenge has been sent. May you conquer all your enemies.")

    except:
        print("Unfortunately, something went wrong. Your challenge could not be sent.")
        print("Double check that the email is valid if you want to send a challenge!")

def accept_challenge(code):
    challenger = ""
    for char in code:
        if char.isdigit() == False:
            challenger += char
        else:
            break
    
    num_digits = len(code) - len(challenger) - 51
    time_start = len(challenger) + 25
    time_end = time_start + num_digits
    final_time = code[time_start:time_end]

    gamemode = code[len(code) - 1]

    return [gamemode, challenger, final_time]

print("***********************************")
print("              CSTRIS               ")
print("***********************************")
name = input("Please enter your name: ")
print("***********************************")
print("Welcome to Cstris, " + name + "!")
choice = display_menu()
if choice == 1:
    print("Please select gamemode: ")
    gamemode = display_gamemodes()
    print("Starting game...")
    final_time = start_game(gamemode, None, None, False)
    print(str(round(final_time,2)) + " seconds! Nice job!")
elif choice == 2:
    email = input("Please enter the email address to send a challenge to: ")
    print("Please select gamemode: ")
    gamemode = display_gamemodes()
    print("Starting game...")
    final_time = start_game(gamemode, None, None, False)
    send_challenge(name, email, final_time, gamemode)
elif choice == 3:
    code = input("Please copy and paste the code you received in your email...\n")
    challenge_info = []
    challenge_info = accept_challenge(code)
    final_time = start_game(int(challenge_info[0]), challenge_info[1], float(challenge_info[2]), True)
elif choice == 4:
    print("Exiting...")
    exit()
