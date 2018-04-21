import pygame
from random import randint
import os
import time
import math

red = (255,0,0)
green = (0,255,0)
darkGreen = (0,127,0)
blue = (0,0,255)
black = (0,0,0)
darkGrey = (64,64,64)
grey = (127,127,127)
white = (255,255,255)
pibotcolor = (52,152,219)
pibotbetacolor = (155,89,182)
xpos = 0
ypos = 0
xaxis = 0
yaxis = 0
angle = 0

width = 640
height = 480

velocity = 0

frames = []

os.system('cls')
print('Starting...')
pygame.init()

mainFont = pygame.font.Font(None, 16)
dispOut = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()

pygame.display.set_caption('idkwhattocallthegameyet')

playerCar = pygame.image.load('playerCar.png')
map = pygame.Surface((1024,1024))
map.fill(white)
tiles = pygame.image.load('tiles.png')

def dispText(msg,color,posy,posx):
	textOut = mainFont.render(msg, True, color)
	dispOut.blit(textOut, [posx, posy])
	
	
def doNothing():
	variable = 0
	
def loadMap(mapFile):
	file = open(mapFile).read()
	lines = file.split("\n")
	print(lines)
	mapOut = []
	for line in lines:
		lineToAdd = []
		items = line.split(" ")
		for item in items:
			try:
				lineToAdd.append(int(item))
			except:
				doNothing
		mapOut.append(lineToAdd)
	print(mapOut)
	return mapOut
	
Exit = False

tileMap = loadMap("test.map")

for line in range(len(tileMap)):
		for point in range(len(tileMap[line])):
			map.blit(tiles, [line*32,(point)*32], [(tileMap[line][point]%16)*32,(tileMap[line][point]//16)*32,32,32])

while not Exit:
	t = time.time()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Exit = True
			print('Closing...')
		if event.type == pygame.MOUSEMOTION:
			mousey = event.pos[0]
			mousex = event.pos[1]
		if event.type == pygame.JOYBUTTONDOWN:
			print(event.button)
		
	##print(velocity)
		
	##xaxis = pygame.key.get_pressed()[pygame.K_UP] - pygame.key.get_pressed()[pygame.K_DOWN]
	##yaxis = pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT]
	if pygame.mouse.get_pressed()[0] == 1:
		if mousex > (height/3)*2:
			xaxis = -1
		elif mousex < height/3:
			xaxis = 1
		else:
			xaxis = 0
		if mousey < width/3:
			yaxis = -1
		elif mousey > (width/3)*2:
			yaxis = 1
		else:
			yaxis = 0
		if int(math.atan2(yaxis,xaxis)/math.pi*180) < 0:
			angle = int((int(math.atan2(yaxis,xaxis)/math.pi*180) + 360)/45)
		else:
			angle = int(int(math.atan2(yaxis,xaxis)/math.pi*180)/45)
		velocity = velocity + 0.5
		
	xpos = xpos + (xaxis * velocity)
	ypos = ypos + (yaxis * velocity)
	
	dispOut.fill(black)
	if velocity > 0.1:
		velocity = velocity * 0.95
	else:
		velocity = 0
	dispOut.blit(map, [-ypos,xpos])
	dispOut.blit(playerCar, [288,208],[angle*64,0,64,64])
	clock.tick(30)
	dispText(str(int(1/(time.time() - t))),white,0,0)
	pygame.display.update()

pygame.quit()
os.system('cls')
quit()
