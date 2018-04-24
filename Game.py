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
realAngle = 0

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

pygame.display.set_caption('i failed this time, maybe next time...')

playerCar = pygame.image.load('playerCar.png')
vignette = pygame.image.load('vignette.png')
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

yrot = [0,0.7,1,0.7,0,-0.7,-1,-0.7]
xrot = [1,0.7,0,-0.7,-1,-0.7,0,0.7]
			
while not Exit:
	t = time.time()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Exit = True
			print('Closing...')
		if event.type == pygame.MOUSEMOTION:
			mousey = event.pos[0] - width / 2
			mousex = event.pos[1] - height / 2
	
	if pygame.key.get_pressed()[pygame.K_UP] == 1:
		velocity = velocity + 0.5
	if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
		velocity = velocity - 0.3
		
	angle = int(realAngle) % 8
		 
	xpos = xpos + (xrot[angle] * velocity)
	ypos = ypos + (yrot[angle] * velocity)
	
	dispOut.fill(black)
	if abs(velocity) > 0.1:
		velocity = velocity * 0.95
		if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
			realAngle = realAngle + 0.1
		if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
			realAngle = realAngle - 0.1
	else:
		velocity = 0
	dispOut.blit(map, [-ypos,xpos])
	dispOut.blit(playerCar, [288,208],[angle*64,0,64,64])
	clock.tick(30)
	dispOut.blit(vignette, [0,0])
	dispText(str(int(1/(time.time() - t))),white,0,0)
	pygame.display.update()

pygame.quit()
os.system('cls')
quit()
