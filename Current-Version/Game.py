import pygame
import random
import os
import time
import math
import json

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
xvels = []
yvels = []
xaxis = 0
yaxis = 0
angle = 0
realAngle = 0
eventCounter = 0

smoothing = 10

width = 640
height = 480

velocity = 0

lastPressed = 0

buttons = {}

if "settings.json" in os.listdir():
	f = open("settings.json","r")
	c = f.read()
	try:
		options = json.loads(c)
	except:
		options = {
			"showFps": False,
			"showVignette": False
			}
	f.close()

settingsButtons = {
	"showVignette": {
		"xpos": 240,
		"ypos": 32,
		"xsize": 100,
		"ysize": 16
		},
	"showFps": {
		"xpos": 240,
		"ypos": 48,
		"xsize": 100,
		"ysize": 16
		},
	"close": {
		"xpos": 0,
		"ypos": 448,
		"xsize": 164,
		"ysize": 16
		},
	"quit": {
		"xpos": 0,
		"ypos": 464,
		"xsize": 148,
		"ysize": 16
		}
	}

print('Starting...')
pygame.init()

mainFont = pygame.font.Font('assets/fonts/PressStart2P.ttf', 16)
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()

pygame.display.set_caption('i failed this time, maybe next time...')

playerCar = pygame.image.load('assets/textures/playerCar.png')
vignette = pygame.image.load('assets/textures/vignette.png')
tiles = pygame.image.load('assets/textures/tiles.png')
settingBackground = pygame.image.load('assets/textures/settings.png')

map = None

def startGame():
	global map
	map = loadMap(mapMenu())

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

def addButton(name,xpos,ypos,xsize,ysize):
	buttons = {}
	buttons[name]["xpos"] = xpos
	buttons[name]["ypos"] = ypos
	buttons[name]["xsize"] = xsize
	buttons[name]["ysize"] = ysize
	return buttons

def dispText(msg,color,posy,posx):
	textOut = mainFont.render(msg, True, color)
	screen.blit(textOut, [posx, posy])

def doNothing():
	variable = 0

def loadMap(mapFile):
	screen.fill(darkGrey)
	dispText("Loading Map...",white,height-26,0)
	file = open(mapFile).read()
	lines = file.split("\n")
	tileMap = []
	for lineNum in range(len(lines)):
		completion = (lineNum + 1) / len(lines)
		lineToAdd = []
		items = lines[lineNum].split(" ")
		for item in items:
			try:
				lineToAdd.append(int(item))
			except:
				doNothing
		tileMap.append(lineToAdd)
		screen.fill(white, rect=[0,height-10,completion*width,height])
		updateAll()
	mapOut = pygame.Surface((len(tileMap)*32-32,len(tileMap[0])*32-32))
	mapOut.fill(white)
	screen.fill(darkGrey)
	dispText("Rendering Map...",white,height-26,0)
	for line in range(len(tileMap)):
		completion = (line+1) / len(tileMap)
		for point in range(len(tileMap[line])):
			mapOut.blit(tiles, [(line)*32,(point)*32], [(tileMap[line][point]%16)*32,(tileMap[line][point]//16)*32,32,32])
		screen.fill(white, rect=[0,height-10,completion*width,height])
		updateAll()
	return mapOut.copy()


Exit = False

def settingsMenu():
	global options, Exit, settingsButtons
	temp = screen.copy()
	settings = True
	while settings:
		screen.blit(temp,(0,0))
		screen.blit(settingBackground,(0,0))
		dispText("PAUSED:",(255,255,255),0,0)
		dispText("Vignette:",(255,255,255),32,0)
		dispText("Show Fps:",(255,255,255),48,0)
		dispText("Close Menu",(255,255,255),448,0)
		dispText("Quit Game",(255,255,255),464,0)
		dispText(str(options["showVignette"]),(255,255,255),32,240)
		dispText(str(options["showFps"]),(255,255,255),48,240)
		pressed = updateAll(settingsButtons)
		if pressed:
			for b in pressed:
				if b == "showFps":
					options["showFps"] = not options["showFps"]
				if b == "showVignette":
					options["showVignette"] = not options["showVignette"]
				if b == "close":
					settings = False
				if b == "quit":
					Exit = True
					settings = False
					print('Closing...')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Exit = True
				settings = False
				print('Closing...')
			if event.type == pygame.MOUSEMOTION:
				mousey = event.pos[0] - width / 2
				mousex = event.pos[1] - height / 2
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					settings = False
	f = open("settings.json","w")
	f.write(json.dumps(options, indent = "\t"))
	f.close()

def mapMenu():
	global options, Exit, settingsButtons, width
	temp = screen.copy()
	chooseMap = True
	while chooseMap:
		screen.blit(temp,(0,0))
		screen.blit(settingBackground,(0,0))
		chooseMapButtons = {}
		position = 0
		for file in os.listdir():
			if file.endswith(".map"):
				chooseMapButtons[file] = {
					"xpos": 0,
					"ypos": position,
					"xsize": width,
					"ysize": 16
					}
				dispText(file,(255,255,255),position,0)
				position = position + 16
		pressed = updateAll(chooseMapButtons)
		if pressed:
			for button in pressed:
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

yrot = [0,0.7,1,0.7,0,-0.7,-1,-0.7]
xrot = [1,0.7,0,-0.7,-1,-0.7,0,0.7]

startGame()
			
while not Exit:
	t = time.time()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Exit = True
			print('Closing...')
		if event.type == pygame.MOUSEMOTION:
			mousey = event.pos[0] - width / 2
			mousex = event.pos[1] - height / 2
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
				eventCounter = 0
			if event.key == pygame.K_m:
				startGame()
				xpos = 0
				ypos = 0
				xaxis = 0
				yaxis = 0
				angle = 0
				realAngle = 0
				eventCounter = 0
				velocity = 0
				xvels = []
				yvels = []
			if event.key == pygame.K_r:
				xpos = 0
				ypos = 0
				xaxis = 0
				yaxis = 0
				angle = 0
				realAngle = 0
				eventCounter = 0
				velocity = 0
				xvels = []
				yvels = []
			if event.key == pygame.K_ESCAPE:
				settingsMenu()
	
	if eventCounter > 0:
		eventCounter = eventCounter - 1
	
	if pygame.key.get_pressed()[pygame.K_UP] == 1 or pygame.key.get_pressed()[pygame.K_w] == 1:
		velocity = velocity + 1.2
	if pygame.key.get_pressed()[pygame.K_DOWN] == 1 or pygame.key.get_pressed()[pygame.K_s] == 1:
		velocity = velocity - 0.4
	
	xvels = [xrot[angle] * velocity] + xvels
	yvels = [yrot[angle] * velocity] + yvels
	xpos += sum(xvels) / float(len(xvels))
	ypos += sum(yvels) / float(len(yvels))
	
	if len(xvels) >= smoothing:
		del xvels[-1]
	if len(yvels) >= smoothing:
		del yvels[-1]
	
	screen.fill((0,0,0,16))
	
	if velocity < 0:
		direction = -1
	else:
		direction = 1
	
	if abs(velocity) > 0.1:
		velocity = velocity * 0.97
		if eventCounter == 0:
			if pygame.key.get_pressed()[pygame.K_RIGHT] == 1 or pygame.key.get_pressed()[pygame.K_d] == 1:
				angle = angle + direction
				eventCounter = 10
				velocity = velocity * 0.7
			if pygame.key.get_pressed()[pygame.K_LEFT] == 1 or pygame.key.get_pressed()[pygame.K_a] == 1:
				angle = angle - direction
				eventCounter = 10
				velocity = velocity * 0.7
	else:
		velocity = 0

	angle = int(angle) % 8
		
	screen.blit(map, [(-ypos//2)*2,(xpos//2)*2])
	if pygame.key.get_pressed()[pygame.K_SPACE] == 1 and random.randrange(0,10) < velocity:
		map.blit(playerCar, [289+(ypos),210+(-xpos)],[angle*64,64,64,64])
		velocity = velocity * 0.9
	screen.blit(playerCar, [288,208],[angle*64,64,64,64])
	screen.blit(playerCar, [288,208],[angle*64,0,64,64])
	clock.tick(30)
	if options["showVignette"]:
		screen.blit(vignette, [0,0])
	if options["showFps"]:
		dispText(str(int(1/(time.time() - t))),white,0,0)
	dispText("Velocity: "+str(round((velocity/3.0188)*2.23694,2))+"mph",white,464,0)
	updateAll()

pygame.quit()
quit()
