#importing modules

import random
import pygame
pygame.init()

#screen variales
WIDTH,HEIGHT=600,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SNAKE GAME USING PYGAME MODULE ! ")
rows = 20
DRAWGRID = False  # may be changed to True if interested in drawing the grid of the game

#FONTS
SCORE_FONT = pygame.font.SysFont("Arial Black",30)

#OOP IMPLEMENTATION OF SNAKE GAME
class cube(object):
	rows = 20
	w = 600
	def __init__(self,start,dirnx = 1,dirny = 0, color = (255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color
	def move(self,dirnx,dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0]+self.dirnx,self.pos[1]+self.dirny)
	def draw(self,surface,eyes=False):
		gap=self.w//self.rows
		i=self.pos[0]
		j=self.pos[1]
		pygame.draw.rect(surface,self.color,(i*gap + 1,j*gap + 1 ,gap - 2,gap -2))

		#for drawing the eyes of the snake
		if eyes:
			centre = gap//2 
			radius = 3
			circleMiddle1=(i*gap+centre-radius,j*gap+8)
			circleMiddle2=(i*gap+gap-radius*2,j*gap+8)	
			pygame.draw.circle(surface, (0,0,0), circleMiddle1, radius)
			pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):	
	body = []
	turns = {}  # for tracking the turns of the snake
	def __init__(self,color,pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirnx=1
		self.dirny=1
	def move(self):
		global run
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run=False
				break
			keys=pygame.key.get_pressed()

			#conditions for moving the head of the snake
			if keys[pygame.K_LEFT] and self.head.dirnx!=1:
				self.dirnx = -1
				self.dirny = 0
				self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]				
			if keys[pygame.K_RIGHT] and self.head.dirnx !=-1:
				self.dirnx=1
				self.dirny=0
				self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]				
			if keys[pygame.K_DOWN] and self.head.dirny!=-1:
				self.dirnx=0
				self.dirny=1
				self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]				
			if keys[pygame.K_UP] and self.head.dirny!=1:
				self.dirnx=0
				self.dirny=-1
				self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]

		for i,c in enumerate(self.body):
			p = c.pos[:]
			#condition for the other segments of the snake
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				#if the snake crossed the border of the screen then the game would get reset
				if c.pos[0]<=0 or c.pos[0]>=c.rows-1 or  c.pos[1]>=c.rows-1 or c.pos[1]<=0: 
					show_score()
					pygame.time.delay(2000)
					self.reset((1,rows//2))
					return
				else: c.move(c.dirnx,c.dirny)

	def reset(self,pos):
		global score
		score = 0
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny
 
		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
		self.body[-1].dirnx = dx
		self.body[-1].dirny=dy	
       
			
	def draw(self,surface):
		for i,c in enumerate(self.body):
			if i==0:
				c.draw(surface,True)
			else:
				c.draw(surface)

def randomSnack(rows,item):
	'''Method for drawing random snacks'''
	positions = item.body
	while True:
		x=random.randrange(1,rows-1)
		y=random.randrange(1,rows-1)
		if len(list(filter(lambda z:z.pos ==(x,y),positions)))>0:
			continue
		else:
			break
	return (x,y)


def drawGrid(width,rows,surface):
	gap=width//rows
	x=0
	y=0
	for l in range(rows):
		x+=gap
		y+=gap
		pygame.draw.line(surface,(255,255,255),(x,0),(x,width))
		pygame.draw.line(surface,(255,255,255),(0,y),(width,y))

def redrawWIndow(surface):
	global s,snack
	surface.fill((0,0,0))

	if DRAWGRID :
		drawGrid(WIDTH , rows , surface)
	s.draw(surface)
	snack.draw(surface)
	pygame.display.update()

def show_score():
	global score,high_score
	WIN.fill((0,0,0))
	text=SCORE_FONT.render("SCORE : "+str(score)+" HIGH SCORE : "+str(high_score),1,(255,255,255))
	WIN.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-text.get_height()//2))
	pygame.display.update()

def main():
	global s,snack,run,score,high_score
	score=0
	high_score=0
	run=True
	clock=pygame.time.Clock()
	s=snake((255,0,0),(1,rows//2))
	snack = cube(randomSnack(rows,s),color=(0,255,0))
	while run:
		pygame.time.delay(50)
		clock.tick(15) 
		s.move()
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows,s),color=(0,255,0))
			score+=10
			if score>high_score:
				high_score=score
		for x in range(1,len(s.body)):
			if s.body[0].pos ==s.body[x].pos:
				show_score()
				pygame.time.delay(2000)
				s.reset((1,rows//2))
				break
		redrawWIndow(WIN)
	pygame.quit()
if __name__ == '__main__':
	main()