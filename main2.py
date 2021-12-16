import pygame
import time
from pygame.locals import *
import random


SIZE = 40
SCREEN_SIZE_X = 1000
SCREEN_SIZE_Y = 700
SCORE_DISPLAY_X = 900
SCORE_DISPLAY_Y = 0


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 23) * SIZE
        self.y = random.randint(0, 10) * SIZE


class Snake:
    def __init__(self, parent_screen, length=1):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [40] * self.length
        self.y = [40] * self.length
        self.direction = 'down'

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increament_length(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


def is_collision(x1, y1, x2, y2):
    if (y1+SIZE > y2) and (y2 >= y1):
        if (x1+SIZE > x2) and (x2 >= x1):
            return True
    return False

def is_collision_one_axis(x1,x2):
    if (x1+SIZE > x2) and (x2>=x1):
        return True
    return False

class Game:
    def __init__(self, score=0):
        pygame.init()
        pygame.mixer.init()
        self.score = score
        self.surface = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    # function responsible on displaying the score at the top right of screenn
    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"score = {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (SCORE_DISPLAY_X, SCORE_DISPLAY_Y))

    def game_over(self):
        self.background_image_load()
        font = pygame.font.SysFont("arial", 30) # font of line 1
        line1 = font.render(f"Game over your score is {self.snake.length}", True, (255, 255, 255))  # line1 and its colour
        self.surface.blit(line1, (200, 300))  #location of line1
        line2 = font.render("To play the game again press enter to close press escape ", True, (255, 255, 255))
        self.surface.blit(line2, (200, 400))  # location of line2
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface,1)

    def background_image_load(self):
        img = pygame.image.load("resources/wp3906249.jbg.webp")
        self.surface.blit(img, (0, 0))

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}")
        pygame.mixer.Sound.play(sound)

    # function to init the game by let the snake move and put the apple on screen and display the score
    def play(self):
        self.background_image_load()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # block to indicate the collision between snake and apple while playing
        if is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increament_length()
            self.apple.move()
            self.play_sound("1_snake_game_resources_ding.mp3")

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("1_snake_game_resources_crash.mp3")
                raise "Game over"

        # snake collide with walls
        if is_collision_one_axis(self.snake.x[0],1000) or is_collision_one_axis(self.snake.x[0],0) or is_collision_one_axis(self.snake.y[0],0) or is_collision_one_axis(self.snake.y[0],700):
            self.play_sound("1_snake_game_resources_crash.mp3")
            raise "Game over"


    # function which calling in main and responsible for detect any keyboard hits and play the game
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pause = False
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    pass
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
