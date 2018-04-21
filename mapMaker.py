import pygame
from random import randint
import os

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

yoffset = 0
xoffset = 0

width = 640
height = 480

tile = 2

os.system('cls')
print('Starting...')
pygame.init()

mainFont = pygame.font.Font('PressStart2P.ttf', 32)
dispOut = pygame.display.set_mode((width,height))

pygame.display.set_caption('Map Editor')

tiles = pygame.image.load('tiles.png')
icons = pygame.image.load('icons.png')

tileMap = []
for line in range(32):
	points = []
	for point in range(32):
		points.append(randint(28,31))
	tileMap.append(points)

def dispText(msg,color,posy,posx):
	textOut = mainFont.render(msg, True, color)
	dispOut.blit(textOut, [posx, posy])
	
def saveMap(name,map):
	file = open(name,"w")
	for line in map:
		lineToWrite = ""
		for point in line:
			lineToWrite = lineToWrite + " " + str(point)
		file.write(lineToWrite + "\n")
	file.close

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

pibotExit = False

while not pibotExit:	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pibotExit = True
			print('Closing...')
			
		if event.type == pygame.MOUSEMOTION:
			ypos = int(event.pos[0]/32)
			xpos = int(event.pos[1]/32)
			print(xpos,ypos)
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if ypos == 18 and xpos == 0:
					saveMap("test.map",tileMap)
				if ypos == 19 and xpos == 0:
					tileMap = loadMap("test.map")
			if event.button == 4:
				tile = tile + 1
			if event.button == 5:
				tile = tile - 1
				
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				yoffset = yoffset + 1
			if event.key == pygame.K_DOWN:
				yoffset = yoffset - 1
			if event.key == pygame.K_LEFT:
				xoffset = xoffset + 1
			if event.key == pygame.K_RIGHT:
				xoffset = xoffset - 1
		
		tile = tile % 256
		print(tile)
			
	dispOut.fill(white)
	for line in range(len(tileMap)):
		for point in range(len(tileMap[line])):
			dispOut.blit(tiles, [(line+xoffset)*32,(point+1+yoffset)*32], [(tileMap[line][point]%16)*32,(tileMap[line][point]//16)*32,32,32])
	if pygame.mouse.get_pressed()[0] == 1:
		tileMap[ypos-xoffset][(xpos-1)-yoffset] = tile
	dispOut.blit(tiles, [ypos*32,xpos*32], [(tile%16)*32,(tile//16)*32,32,32])
	dispOut.fill(black, rect=[0,0,width,32])
	dispOut.blit(tiles, [0,0], [(tile%16)*32,(tile//16)*32,32,32])
	dispOut.blit(icons, [18*32,0], [0,0,64,32])
	dispText(str(tile),white,0,32)
	pygame.display.update()

pygame.quit()
os.system('cls')
quit()
