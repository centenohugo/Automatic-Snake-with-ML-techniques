"""
Code used on the second iteration
"""

import pygame, sys, time, random, csv, arff
#from wekaI import Weka

# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = -1

# Window size
FRAME_SIZE_X = 480
FRAME_SIZE_Y = 480

# Colors (R, G, B)
BLACK = pygame.Color(51, 51, 51)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(204, 51, 0)
GREEN = pygame.Color(204, 255, 153)
BLUE = pygame.Color(0, 51, 102)

# GAME STATE CLASS
class GameState:
    def __init__(self, FRAME_SIZE):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (FRAME_SIZE[0]//10)) * 10, random.randrange(1, (FRAME_SIZE[1]//10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.prev_v = 'DOWN'
        self.prev_h = self.direction

# Game Over
def game_over(game):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, WHITE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/4)
    game_window.fill(BLUE)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(game, 0, WHITE, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def show_score(game, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(game.score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X/8, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

# Move the snake
def move_keyboard(game, event):
    # Whenever a key is pressed down
    change_to = game.direction
    if event.type == pygame.KEYDOWN:
        # W -> Up; S -> Down; A -> Left; D -> Right
        if (event.key == pygame.K_UP or event.key == ord('w')) and game.direction != 'DOWN':
            change_to = 'UP'
        if (event.key == pygame.K_DOWN or event.key == ord('s')) and game.direction != 'UP':
            change_to = 'DOWN'
        if (event.key == pygame.K_LEFT or event.key == ord('a')) and game.direction != 'RIGHT':
            change_to = 'LEFT'
        if (event.key == pygame.K_RIGHT or event.key == ord('d')) and game.direction != 'LEFT':
            change_to = 'RIGHT'
    return change_to

# TODO: IMPLEMENT HERE THE NEW INTELLIGENT METHOD
def move_tutorial_1(game):
    change_to = game.direction
    if game.food_pos[0] > game.snake_pos[0]:
        if can_move(game.snake_pos[0], game.snake_pos[1], 'RIGHT'):
            change_to = 'RIGHT'
            game.prev_h = 'RIGHT'
        else:
            change_to = game.prev_v
    elif game.food_pos[0] == game.snake_pos[0]:
        if game.food_pos[1] > game.snake_pos[1]:
            if can_move(game.snake_pos[0], game.snake_pos[1], 'DOWN'):
                change_to = 'DOWN'
                game.prev_v = 'DOWN'
            else:
                change_to = game.prev_h
        elif game.food_pos[1] < game.snake_pos[1]:
            if can_move(game.snake_pos[0], game.snake_pos[1], 'UP'):
                change_to = 'UP'
                game.prev_v = 'UP'
            else:
                change_to = game.prev_h
    else:
        if can_move(game.snake_pos[0], game.snake_pos[1], 'LEFT'):
            change_to = 'LEFT'
            game.prev_h = 'LEFT'
        else:
            change_to = game.prev_v


    if can_move(game.snake_pos[0], game.snake_pos[1], 'RIGHT') or can_move(game.snake_pos[0], game.snake_pos[1], 'LEFT') or can_move(
            game.snake_pos[0], game.snake_pos[1], 'UP') or can_move(game.snake_pos[0], game.snake_pos[1], 'DOWN'):
        while not can_move(game.snake_pos[0], game.snake_pos[1], change_to):
            change_to = make_decision(game, change_to)
    return change_to

def can_move(pos_x, pos_y, direction):
    next_move=[pos_x, pos_y]
    if direction == 'RIGHT':
        next_move[0] = next_move[0] + 10
    elif direction == 'LEFT':
        next_move[0] = next_move[0] - 10
    elif direction == 'UP':
        next_move[1] = next_move[1] - 10
    elif direction == 'DOWN':
        next_move[1] = next_move[1] + 10

    if next_move not in game.snake_body and next_move[0]>=0 and next_move[0]<FRAME_SIZE_X and next_move[1]>=0 and next_move[
        1]<FRAME_SIZE_Y:
        return True
    else:
        return False

def make_decision(game, direction):

    if direction == 'UP' or direction == 'DOWN':
        if game.prev_h == 'RIGHT' and can_move(game.snake_pos[0],
                                               game.snake_pos[1], 'RIGHT'):
            return 'RIGHT'
        elif can_move(game.snake_pos[0], game.snake_pos[1], 'LEFT'):
            game.prev_h = 'LEFT'
            return 'LEFT'
        elif can_move(game.snake_pos[0], game.snake_pos[1], 'RIGHT'):
            game.prev_h = 'RIGHT'
            return 'RIGHT'
        else:
            return game.prev_h
    elif direction == 'RIGHT' or direction == 'LEFT':
        if game.prev_v == 'UP' and can_move(game.snake_pos[0],
                                            game.snake_pos[1], 'UP'):
            return 'UP'
        elif can_move(game.snake_pos[0], game.snake_pos[1], 'DOWN'):
            game.prev_v = 'DOWN'
            return 'DOWN'
        elif can_move(game.snake_pos[0], game.snake_pos[1], 'UP'):
            game.prev_v = 'UP'
            return 'UP'
        else:
            return game.prev_v
    else:
        return direction

#This method computes the distance until crashing, either with the wall or with itself
def distance_to_crash(game):
    if game.direction == "RIGHT":
        d_to_wall = abs(game.snake_pos[0] - FRAME_SIZE_X) - 10
        d_to_itself = float('inf')
        for sublist in game.snake_body[1:]:
            if sublist[1] == game.snake_pos[1] and sublist[0] >= game.snake_pos[0]:
                d_to_itself = abs(game.snake_pos[0] - sublist[0])
        return min(d_to_wall, d_to_itself)
    elif game.direction == "LEFT":
        d_to_wall = game.snake_pos[0]
        d_to_itself = float('inf')
        for sublist in game.snake_body[1:]:
            if sublist[1] == game.snake_pos[1] and sublist[0] <= game.snake_pos[0]:
                d_to_itself = abs(game.snake_pos[0] - sublist[0])
        return min(d_to_wall, d_to_itself)
    elif game.direction == "UP":
        d_to_wall = game.snake_pos[1]
        d_to_itself = float('inf')
        for sublist in game.snake_body[1:]:
            if sublist[0] == game.snake_pos[0] and sublist[1] <= game.snake_pos[1]:
                d_to_itself = abs(game.snake_pos[1] - sublist[1])
        return min(d_to_wall, d_to_itself)
    #game.direction == "DOWN"
    else:
        d_to_wall = abs(game.snake_pos[1] - FRAME_SIZE_Y) - 10
        d_to_itself = float('inf')
        for sublist in game.snake_body[1:]:
            if sublist[0] == game.snake_pos[0] and sublist[1] >= game.snake_pos[1]:
                d_to_itself = abs(game.snake_pos[1] - sublist[1])
        return min(d_to_wall, d_to_itself)

def relative_head_apple_x(game):
    if game.snake_pos[0] > game.food_pos[0]:
        return "LEFT"
    elif game.snake_pos[0] < game.food_pos[0]:
        return "RIGHT"
    else:
        return "SAME"
def relative_head_apple_y(game):
    if game.snake_pos[1] > game.food_pos[1]:
        return "UP"
    elif game.snake_pos[1] < game.food_pos[1]:
        return "DOWN"
    else:
        return "SAME"

# PRINTING DATA FROM GAME STATE
def print_state(game):
    print("--------GAME STATE--------")
    print("FrameSize:", FRAME_SIZE_X, FRAME_SIZE_Y)
    print("Direction:", game.direction)
    print("Snake X:", game.snake_pos[0], ", Snake Y:", game.snake_pos[1])
    print("Snake Body:", game.snake_body)
    print("Food X:", game.food_pos[0], ", Food Y:", game.food_pos[1])
    print("Score:", game.score)

# Function to format game data into a string
def print_line_data(game):
    current_state_data = [
        str(game.food_pos[0]),
        str(game.food_pos[1]),
        str(game.snake_pos[0]),
        str(game.snake_pos[1]),
        str(len(game.snake_body)),
        str(can_move(game.snake_pos[0], game.snake_pos[1], 'UP')),
        str(can_move(game.snake_pos[0], game.snake_pos[1], 'DOWN')),
        str(can_move(game.snake_pos[0], game.snake_pos[1], 'RIGHT')),
        str(can_move(game.snake_pos[0], game.snake_pos[1], 'LEFT')),
        str(game.score),
        str(game.direction),
        str(distance_to_crash(game)),
        str(relative_head_apple_x(game)),
        str(relative_head_apple_y(game))
    ]

    # 0: UP      2:RIGHT
    # 1: DOWN    3:LEFT
    if move_keyboard(game, event) == 'UP':
        decision = 0
    elif move_keyboard(game, event) == 'DOWN':
        decision = 1
    elif move_keyboard(game, event) == 'RIGHT':
        decision = 2
    else:
        decision = 3
        # manual
        # str(decision)
        # automatic
        # str(make_decision(game, game.direction))
    
    
    #First tick
    if len(game.snake_body) == 3 and game.snake_pos == [110, 50] and game.score == -1:
        with open(arff_file, 'a') as f:  # Open the file in append mode
            f.write(', '.join(current_state_data))  # Write the line followed by a newline character
        print(', '.join(current_state_data))
    #Last tick
    elif ((move_keyboard(game, event) == "UP" and not (can_move(game.snake_pos[0], game.snake_pos[1], 'UP'))) or
          (move_keyboard(game, event) == "DOWN" and not (can_move(game.snake_pos[0], game.snake_pos[1], 'DOWN'))) or
          (move_keyboard(game, event) == "RIGHT" and not (can_move(game.snake_pos[0], game.snake_pos[1], 'RIGHT'))) or
          (move_keyboard(game, event) == "LEFT" and not (can_move(game.snake_pos[0], game.snake_pos[1], 'LEFT')))):
        with open(arff_file, 'a') as f:  # Open the file in append mode
            f.write(', ' + str(game.score) + ', ' + str(decision) + '\n' + ', '.join(current_state_data) + ', ' + str(game.score) + ', ' + str(decision) + '\n')
        print(', '.join(current_state_data))
    else:
        with open(arff_file, 'a') as f:  # Open the file in append mode
            f.write(', ' + str(game.score) + ', ' + str(decision) + '\n' + ', '.join(current_state_data))  # Write the line followed by a newline character
        print(', '.join(current_state_data))

# Checks for errors encounteRED
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater - Machine Learning (UC3M)')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))

#Uncomment once the data is collected and we want to movement to be determined
#by the classification model.
#Weka
#weka = Weka()
#weka.start_jvm()


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Main logic
game = GameState((FRAME_SIZE_X, FRAME_SIZE_Y))

#File where the data will be stored
#modify path if neccesary
arff_file = "G:/Mi unidad/2do Curso Carrera/2do Cuatri/Machine Learning I/Assignments/1/2nd Iteration/train_agent_It2.arff"


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        # CALLING MOVE METHOD
        game.direction = move_keyboard(game, event)

    #Uncomment once we want to movement to be decided by the chosen classification model

    #x = [game.food_pos[0], game.food_pos[1], game.snake_pos[0], game.snake_pos[1], len(game.snake_body),
    #     str(can_move(game.snake_pos[0], game.snake_pos[1], 'UP')),
    #     str(can_move(game.snake_pos[0], game.snake_pos[1], 'DOWN')),
    #     str(can_move(game.snake_pos[0], game.snake_pos[1], 'RIGHT')),
    #    str(can_move(game.snake_pos[0], game.snake_pos[1], 'LEFT')),
    #     game.score,
    #     str(game.direction)
    #     ]
    #a = Weka.predict(weka, "/home/ml-uc3m/PycharmProjects/PythonWeka/J48_trialmodel.model",
    #                 x, "/home/ml-uc3m/PycharmProjects/PythonWeka/test_keyboard_nofuture.arff")

    #The type of the prediction is integer
    #a = int(a)


    #Movement. UNCOMMENT WHEN METHOD IS IMPLEMENTED
    game.direction = move_tutorial_1(game)
    #game.direction = move_keyboard(game, event)
    '''
    if a == 0:
        game.direction = "UP"
    elif a == 1:
        game.direction = "DOWN"
    elif a == 2:
        game.direction = "RIGHT"
    else:
        game.direction = "LEFT"
    '''

    # Moving the snake
    if game.direction == 'UP':
        game.snake_pos[1] -= 10
    if game.direction == 'DOWN':
        game.snake_pos[1] += 10
    if game.direction == 'LEFT':
        game.snake_pos[0] -= 10
    if game.direction == 'RIGHT':
        game.snake_pos[0] += 10

        # Snake body growing mechanism
    game.snake_body.insert(0, list(game.snake_pos))
    if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
        game.score += 100
        game.food_spawn = False
    else:
        game.snake_body.pop()
        game.score -= 1

        # Spawning food on the screen
    if not game.food_spawn:
        game.food_pos = [random.randrange(1, (FRAME_SIZE_X//10)) * 10, random.randrange(1, (FRAME_SIZE_Y//10)) * 10]
    game.food_spawn = True

    # GFX
    game_window.fill(BLUE)
    for pos in game.snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, RED, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if game.snake_pos[0] < 0 or game.snake_pos[0] > FRAME_SIZE_X-10:
        game_over(game)
    if game.snake_pos[1] < 0 or game.snake_pos[1] > FRAME_SIZE_Y-10:
        game_over(game)
    # Touching the snake body
    for block in game.snake_body[1:]:
        if game.snake_pos[0] == block[0] and game.snake_pos[1] == block[1]:
            game_over(game)

    show_score(game, 1, WHITE, 'consolas', 15)

    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(DIFFICULTY)

    #Tests
    print_line_data(game)
    #print(move_keyboard(game, event))
    #print(distance_to_crash(game))
    #print(food_orientation(game))

