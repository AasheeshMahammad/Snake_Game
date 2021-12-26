import random,os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from enum import Enum
from collections import namedtuple

class Directions(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4

class const:
    Point = namedtuple('Point',['x','y'])
    BLOCK_SIZE = 20
    SPEED = 5
    COLORS={"white":(255,255,255),"red":(255,0,0),"black":(0,0,0),
            "blue":(0,0,255),"green":(0,255,0)}
    pygame.font.init()
    FONT=pygame.font.SysFont('arial',19)


class Snake_Game:
    def __init__(self,width=640,height=480) -> None:
        pygame.init()
        self.width=width
        self.height=height

        self.display=pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Snake Game')
        self.clock=pygame.time.Clock()

        self.direction=Directions.RIGHT
        
        self.head=const.Point(self.width/2,self.height/2)
        #print(self.head)
        self.snake=[self.head,const.Point(self.head.x-const.BLOCK_SIZE,self.head.y),
                    const.Point(self.head.x-(2*const.BLOCK_SIZE),self.head.y)]
        self.score=0
        self.food=None
        self._place_food()


    def _place_food(self):
        x=random.randint(0,(self.width-const.BLOCK_SIZE)//const.BLOCK_SIZE)*const.BLOCK_SIZE
        y=random.randint(0,(self.height-const.BLOCK_SIZE)//const.BLOCK_SIZE)*const.BLOCK_SIZE
        self.food=const.Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def play(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Directions.RIGHT:
                    self.direction = Directions.LEFT

                elif event.key == pygame.K_RIGHT and self.direction != Directions.LEFT:
                    self.direction = Directions.RIGHT

                elif event.key == pygame.K_UP and self.direction != Directions.DOWN and self.direction != Directions.UP:
                    self.direction = Directions.DOWN

                elif event.key == pygame.K_DOWN and self.direction != Directions.UP and self.direction != Directions.DOWN:
                    self.direction = Directions.UP
            
        self._move()
        alive=True
        self.snake.insert(0,self.head)    

        if self._collide():
            alive=False
        if self.head == self.food:
            self.score+=1
            self._place_food()
        else:
            self.snake.pop()
        
        self._update()
        self.clock.tick(const.SPEED)

        return alive,self.score
    
    def _collide(self):
        if((self.head.x > self.width - const.BLOCK_SIZE or self.head.x < 0) or (self.head.y > self.height - const.BLOCK_SIZE or self.head.y < 0)):
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _update(self):
        self.display.fill(const.COLORS['black'])
        for pt in self.snake:
            pygame.draw.rect(self.display,const.COLORS['blue'],pygame.Rect(pt.x,pt.y,const.BLOCK_SIZE,const.BLOCK_SIZE))
            pygame.draw.rect(self.display,const.COLORS['green'],pygame.Rect(pt.x+4,pt.y+4,12,12))
        pygame.draw.rect(self.display,const.COLORS['red'],pygame.Rect(self.food.x,self.food.y,const.BLOCK_SIZE,const.BLOCK_SIZE))
        text=const.FONT.render("Score : "+str(self.score),True,const.COLORS['white'])
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def _move(self):
        x,y=self.head.x,self.head.y
        if self.direction == Directions.RIGHT:
            x += const.BLOCK_SIZE
        elif self.direction == Directions.LEFT:
            x -= const.BLOCK_SIZE
        elif self.direction == Directions.UP:
            y += const.BLOCK_SIZE
        elif self.direction == Directions.DOWN:
            y -= const.BLOCK_SIZE
        
        self.head = const.Point(x,y)

if __name__=='__main__':
    game=Snake_Game()
    while True:
        try:
            alive,score=game.play()
            if not alive:
                break
        except KeyboardInterrupt:
            break
    print("Score :",score)
    pygame.quit()