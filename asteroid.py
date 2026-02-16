import pygame
import sys 

from random import randint , uniform

def laser_update(laser_list , speed = 300):
	for rect in laser_list:
		rect.y -= speed * dt
		if rect.bottom < 0:
			laser_list.remove(rect)

def meteor_update(meteor_list, speed = 300):
	for meteor_tuple in meteor_list:
		
		direction = meteor_tuple[1]
		meteor_rect = meteor_tuple[0]

		meteor_rect.center += direction * speed * dt 
		if meteor_rect.top > WINDOW_HEIGHT: 
			meteor_list.remove(meteor_tuple)




def display_score():
	# with the 100 (in seconds) ... it millisecs
	score_text = f'Score: {pygame.time.get_ticks() // 1000}'
	text_surf = font.render(score_text, True, (255,255,255))
	text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2 , WINDOW_HEIGHT - 80))
	display_surface.blit(text_surf, text_rect)
	pygame.draw.rect(display_surface, (255,255,255), text_rect.inflate(30,30), width = 8 , border_radius = 4)
	

def laser_timer(can_shoot, duration = 500):
	if not can_shoot:
		current_time = pygame.time.get_ticks()
		if current_time - shoot_time > duration:
			can_shoot = True
	return can_shoot




# game init
pygame.init()
WINDOW_WIDTH , WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
# use method to change title of the window
pygame.display.set_caption("Asteriod Shootter")
clock = pygame.time.Clock()

#   ship importing images
ship_surf = pygame.image.load("C:/Users/jd/Downloads/asteroid_shooter_files/asteroid_shooter_files/project_3 - Placing elements/graphics/ship.png").convert_alpha()
ship_y_pos = 500
ship_rect = ship_surf.get_rect( center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

#background
# import the background and blit it on the display surface
bg_surf = pygame.image.load("C:/Users/jd/Downloads/asteroid_shooter_files/asteroid_shooter_files/project_1 - blank window/graphics/background.png").convert_alpha()

# laser import
#1. import the laser surface and create a rect
#2. rect start pos -> at the top of the ship
laser_surf = pygame.image.load("C:/Users/jd/Downloads/asteroid_shooter_files/asteroid_shooter_files/project_1 - blank window/graphics/laser.png").convert_alpha()
laser_list = []

# laser time
can_shoot = True
shoot_time = None

#laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)

# import text
font = pygame.font.Font("C:/Users/jd/Downloads/asteroid_shooter_files/asteroid_shooter_files/project_10 - Delta/graphics/subatomic.ttf",50)


#meteor
meteor_surf = pygame.image.load("C:/Users/jd/Downloads/AsteriodGame/meteor.png").convert_alpha()
meteor_list = []

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)


# drawing
test_rect = pygame.Rect(100,200,400,500)
# keeps the code going
# GAME LOOP

# import sound
laser_sound = pygame.mixer.Sound("C:/Users/jd/Downloads/asteroid_shooter_files/asteroid_shooter_files/project_4 - Image Text/sounds/laser.ogg")
explosion_sound = pygame.mixer.Sound("C:/Users/jd/Downloads/asteroid_shooter_files/asteroid_shooter_files/project_4 - Image Text/sounds/explosion.wav")
background_music = pygame.mixer.Sound("C:/Users/jd/Downloads/asteroid_shooter_files/asteroid_shooter_files/project_4 - Image Text/sounds/music.wav")


background_music.play(loops = -1)
while True: #run forever ... keep out game runnin

	# event loop
	# DONT RUN THE CODE TIL I TELL YOU
	 #1. input ... events( mouse clicks, press a button...)
	 for event in pygame.event.get():
	 	if event.type == pygame.QUIT:
	 		pygame.quit()
	 		sys.exit()

	 	if event.type == pygame.MOUSEBUTTONDOWN and can_shoot: # 0.5 seconds of delay before we can shoot again 
	 		# laser
	 		laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
	 		laser_list.append(laser_rect)

	 		# timer 
	 		can_shoot = False
	 		shoot_time = pygame.time.get_ticks()

	 		# play laser sound
	 		laser_sound.play()

	 	if event.type == meteor_timer:
	 		
	 		# random position
	 		x_pos = randint(-100, WINDOW_WIDTH + 100)
	 		y_pos = randint(-100, -50)

	 		meteor_rect = meteor_surf.get_rect(center = (x_pos, y_pos))
	 		
	 		# create a rect
	 		meteor_rect = meteor_surf.get_rect(center = (x_pos, y_pos))
	 		
	 		# create a random direction
	 		direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
	 		meteor_list.append((meteor_rect, direction))
	 	

	 # framerate limit
	 dt = clock.tick(120) / 1000 # 12 millisecs

	 # mouse input
	 ship_rect.center = pygame.mouse.get_pos()

	 # update
	 # move the laser upwards
	 # 10 no movement
	 # 200 faster movement
	 
	 laser_update(laser_list)
	 meteor_update(meteor_list)
	 can_shoot = laser_timer(can_shoot, 2000)
	 

	 # metoer ship collison
	 for meteor_tuple in meteor_list:
	 	meteor_rect = meteor_tuple[0]
	 	if ship_rect.colliderect(meteor_rect):
	 		print("Collision")
	 		pygame.quit()
	 		sys.exit()

	 # laser meteor collisions
	 # we need 2 for loop ... ones for the meteor and one for the laser
	 for laser_rect in laser_list:
	 	for meteor_tuple in meteor_list:
	 		if laser_rect.colliderect(meteor_tuple[0]):
	 			meteor_list.remove(meteor_tuple)
	 			laser_list.remove(laser_rect)
	 			print("Score ")
	 			explosion_sound.play()

	 # DRAWING
	 #2. updates
	 display_surface.fill((0,0, 0))
	 display_surface.blit(bg_surf, (0,0))

	 display_score()
	# if ship_rect.y > 0:
	# 	ship_rect.y -= 4
	
	 # blit the laser
	 # loop that draws the laser surface where the rect are
	 for rect in laser_list:
	 	display_surface.blit(laser_surf, rect)

	 for meteor_tuple in meteor_list:
	 	display_surface.blit(meteor_surf, meteor_tuple[0])

	 display_surface.blit(ship_surf, ship_rect)
	

	 # draw the final frame
	 #3. show the frame to player / update display surface
	 pygame.display.update()
	 #print(len(laser_list))