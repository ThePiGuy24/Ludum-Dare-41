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

tile = 1

print('Starting...')
pygame.init()

mainButtons = {
	"save": {
		"xpos": 576,
		"ypos": 0,
		"xsize": 32,
		"ysize": 32
		},
	"load": {
		"xpos": 608,
		"ypos": 0,
		"xsize": 32,
		"ysize": 32
		}
	}

mainFont = pygame.font.Font('assets/fonts/PressStart2P.ttf', 32)
mainFont2 = pygame.font.Font('assets/fonts/PressStart2P.ttf', 16)
screen = pygame.display.set_mode((width,height))

pygame.display.set_caption('Map Editor')

tiles = pygame.image.load('assets/textures/tiles.png')
icons = pygame.image.load('assets/textures/icons.png')
settingBackground = pygame.image.load('assets/textures/settings.png')

def dispTile(tile,xpos,ypos):
	screen.blit(tiles, [ypos*32,xpos*32], [(tile%16)*32,(tile//16)*32,32,32])

def dispText(msg,color,posy,posx):
	textOut = mainFont.render(msg, True, color)
	screen.blit(textOut, [posx, posy])
	
def dispText2(msg,color,posy,posx):
	textOut = mainFont2.render(msg, True, color)
	screen.blit(textOut, [posx, posy])

def updateAll(buttons = {}):
	global lastPressed
	pressed = []
	mousex, mousey = pygame.mouse.get_pos()
	for button in buttons:
		if buttons[button]["xpos"] < mousex < buttons[button]["xsize"] + buttons[button]["xpos"] and buttons[button]["ypos"] < mousey and mousey < buttons[button]["ysize"] + buttons[button]["ypos"]:
			if lastPressed == 0 and pygame.mouse.get_pressed()[0]:
				lastPressed = 1
				pressed.append(button)
			pygame.draw.rect(screen, (255,255,255), [buttons[button]["xpos"],buttons[button]["ypos"],buttons[button]["xsize"]-1,buttons[button]["ysize"]-1], 2)
	pygame.display.update()
	if not pygame.mouse.get_pressed()[0]:
		lastPressed = 0
	return pressed
	
def saveMap(name,map):
	file = open(name,"w")
	for line in map:
		lineToWrite = ""
		for point in line:
			lineToWrite = lineToWrite + " " + str(point)
		file.write(lineToWrite + "\n")
	file.close

def mapMenu():
	global options, Exit, settingsButtons, width
	temp = screen.copy()
	chooseMap = True
	while chooseMap:
		screen.blit(temp,(0,0))
		screen.blit(settingBackground,(0,0))
		chooseMapButtons = {}
		position = 0
		chooseMapButtons["new"] = {
			"xpos": 0,
			"ypos": position,
			"xsize": width,
			"ysize": 16
			}
		dispText2("Create New Map",(255,255,255),position,0)
		position = 16
		for file in os.listdir():
			if file.endswith(".map"):
				chooseMapButtons[file] = {
					"xpos": 0,
					"ypos": position,
					"xsize": width,
					"ysize": 16
					}
				dispText2(file,(255,255,255),position,0)
				position = position + 16
		pressed = updateAll(chooseMapButtons)
		if pressed:
			for button in pressed:
				if button == "new":
					chosenmap = []
					for line in range(64):
						points = []
						for point in range(64):
							points.append(randint(28,31))
						chosenmap.append(points)
					chooseMap = False
				else:
					chosenmap = button
					chooseMap = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEMOTION:
				mousey = event.pos[0] - width / 2
				mousex = event.pos[1] - height / 2
	return chosenmap

def fileSelect():
	file = mapMenu()
	if type(file) == type("string"):
		return loadMap(file)
	else:
		return file
	
def loadMap(mapFile):
	file = open(mapFile).read()
	lines = file.split("\n")
	mapOut = []
	for line in lines:
		lineToAdd = []
		items = line.split(" ")
		for item in items:
			try:
				lineToAdd.append(int(item))
			except:
				continue
		mapOut.append(lineToAdd)
	return mapOut

Exit = False

tileMap = fileSelect()

while not Exit:	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Exit = True
			print('Closing...')
			
		if event.type == pygame.MOUSEMOTION:
			ypos = int(event.pos[0]/32)
			xpos = int(event.pos[1]/32)
			
		if event.type == pygame.MOUSEBUTTONDOWN:
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
			if event.key == pygame.K_KP_PLUS:
				tile = tile + 1
			if event.key == pygame.K_KP_MINUS:
				tile = tile - 1
		
		tile = tile % 256
			
	screen.fill(white)
	for line in range(len(tileMap)):
		for point in range(len(tileMap[line])):
			screen.blit(tiles, [(line+xoffset)*32,(point+1+yoffset)*32], [(tileMap[line][point]%16)*32,(tileMap[line][point]//16)*32,32,32])
	if pygame.mouse.get_pressed()[0] == 1 and xpos > 0 and 0 <= yoffset < 64 and 0 <= xoffset < 64:
		tileMap[ypos-xoffset][(xpos-1)-yoffset] = tile
	dispTile(tile, xpos, ypos)
	screen.fill(black, rect=[0,0,width,32])
	dispTile(tile, 0, 0)
	screen.blit(icons, [18*32,0], [0,0,64,32])
	dispText(str(tile),white,0,32)
	pressedButtons = updateAll(mainButtons)
	if pressedButtons:
		if "load" in pressedButtons:
			tileMap = fileSelect()
			xpos = 0
			ypos = 0
			yoffset = 0
			xoffset = 0
			tile = 1
		elif "save" in pressedButtons:
			print("test")

pygame.quit()
quit()
