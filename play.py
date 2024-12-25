import pygame
from pygame.locals import *
import time
import random

SIZE=40

BACKGROUND_COLOR=(55, 255, 0)

class Apple:
    def __init__(self,pareant_screan):
        self.image=pygame.image.load("C:\\Rohit\\Games\\Snake Game\\apple.jpg").convert()
        self.pareant_screen=pareant_screan
        self.x=SIZE*3
        self.y=SIZE*3

    def draw(self):
        self.pareant_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.x=random.randint(1,24)*SIZE
        self.y=random.randint(1,14)*SIZE

class Snake:
    def __init__(self,pareant_screan,length):
        self.length=length
        self.parent_screan=pareant_screan
        self.block=pygame.image.load("C:\\Rohit\\Games\\Snake Game\\block.jpg").convert()
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='down'

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screan.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=="up":
            self.y[0]-=SIZE
        if self.direction=="down":
            self.y[0]+=SIZE
        if self.direction=="left":
            self.x[0]-=SIZE
        if self.direction=="right":
            self.x[0]+=SIZE
        self.draw()


    def move_left(self):
        self.direction='left'

    def move_right(self):
        self.direction='right'

    def move_up(self):
        self.direction='up'

    def move_down(self):
        self.direction='down'


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface=pygame.display.set_mode((1040,600))
        self.surface.fill((29, 0, 247))
        self.snake=Snake(self.surface, 3)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True
            return False

    def play_background_music(self):
        pygame.mixer.music.load("C:\\Rohit\\Games\\Snake Game\\bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_Sound(self,sound):
        sound=pygame.mixer.Sound(f"C:\\Rohit\\Games\\Snake Game\\{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg=pygame.image.load("C:\\Rohit\\Games\\Snake Game\\background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()


#   Snake Eating Apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_Sound("ding")
            self.snake.increase_length()
            self.apple.move()

#   snake collideing itself
        for i in range(1,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_Sound("crash")
                raise "Game Over"

        if not (0<=self.snake.x[0]<=1000 and 0<=self.snake.y[0]<=571):
            self.play_Sound('crash')
            raise "hit the boundry error"

    def show_game_over(self):
        self.render_background()
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is over! Your score is {self.snake.length-3}",True,(186, 0, 0))
        self.surface.blit(line1,(200,300))
        line2=font.render("To play again press Enter.To exit press Escape!",True,(186, 0, 0))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()


    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"Score: {self.snake.length-3}",True,(0,0,0))
        self.surface.blit(score,(875,20))

    def reset(self):
        self.snake=Snake(self.surface, 3)
        self.apple=Apple(self.surface)

    def run(self):
            running=True
            pause=False

            while running:
                for event in pygame.event.get():
                    if event.type==KEYDOWN:
                        if event.key==K_ESCAPE:
                            running=False

                        if event.key==K_RETURN:
                            pygame.mixer.music.unpause()
                            pause=False

                        if not pause:
                            if event.key==K_UP:
                                self.snake.move_up()

                            if event.key==K_DOWN:
                                self.snake.move_down()

                            if event.key==K_RIGHT:
                                self.snake.move_right()

                            if event.key==K_LEFT:
                                self.snake.move_left()

                    elif event.type==QUIT:
                        running=False
                try:
                    if not pause:
                        self.play()
                except Exception as e:
                    self.show_game_over()
                    pause=True
                    self.reset()

                time.sleep(0.3)

if __name__=="__main__":
    game=Game()
    game.run()