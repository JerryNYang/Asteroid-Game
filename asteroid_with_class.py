import pygame
import sys 
from random import randint, uniform


class Ship(pygame.sprite.Sprite):
	def __init__(self , groups):
		# 1. we have to init the parent class
		super().__init__(groups)

		# 2. We need a surface -> image
		self.image = pygame.image.load("../AsteriodGame/ship.png").convert_alpha()

		#3. we need a rect
		self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
	
		# 4. add a mask
		self.mask = pygame.mask.from_surface(self.image)

		# timer
		self.can_shoot = True
		self.shoot_time = None

		# sound 
		self.laser_sound = pygame.mixer.Sound("./sounds/laser.ogg")

	def laser_time(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > 500:
				self.can_shoot = True

	def input_position(self):
		pos = pygame.mouse.get_pos()
		self.rect.center = pos 

	def laser_shoot(self):
		if pygame.mouse.get_pressed()[0] and self.can_shoot == True:
			self.can_shoot = False
			self.shoot_time = pygame.time.get_ticks()

			Laser(self.rect.midtop, laser_group)
			self.laser_sound.play()

	def meteor_collision(self):
		# self is ship sprite
		if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
			pygame.quit()
			sys.exit()



	def update(self):
		self.laser_time()
		self.laser_shoot()
		self.input_position()
		self.meteor_collision()

class Laser(pygame.sprite.Sprite):
	def __init__(self , pos, groups):
		# 1. we have to init the parent class
		super().__init__(groups)

		# 2. We need a surface -> image
		self.image = pygame.image.load("../AsteriodGame/laser.png").convert_alpha()

		#3. we need a rect
		self.rect = self.image.get_rect(midbottom = pos)
		# 4. add a mask
		self.mask = pygame.mask.from_surface(self.image)


		# float based position
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(0,-1)
		self.speed = 600

		# sound 
		self.explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")


	def meteor_collision(self):
		# self is ship sprite
		if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
			self.kill()
			self.explosion_sound.play()


	def update(self):
		self.pos += self.direction * self.speed * dt
		self.rect.topleft = (round(self.pos.x) , round(self.pos.y))
		
		# memory efficiency
		if self.rect.bottom < 0:
			self.kill()

		self.meteor_collision()
		
class Meteor(pygame.sprite.Sprite):
	def __init__(self , pos, groups):

		# basic setup
		# 1. we have to init the parent class
		super().__init__(groups)
		# 2. We need a surface -> image
		meteor_surf = pygame.image.load("../AsteriodGame/meteor.png").convert_alpha()
		meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5,1.5)
		self.scale_surf = pygame.transform.scale(
			meteor_surf,
			meteor_size)

		self.image = self.scale_surf

		#3. we need a rect
		# float based positioning
		self.rect = self.image.get_rect(center = pos)
		self.mask = pygame.mask.from_surface(self.image)

		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
		self.speed = randint(200,500)

		# rotation logic
		self.rotation = 0
		self.rotation_speed = randint(20,46)

	def rotate(self):
		self.rotation += self.rotation_speed * dt
		rotated_surf = pygame.transform.rotozoom(self.scale_surf, self.rotation, 1)
		self.image = rotated_surf
		self.rect = self.image.get_rect(center = self.rect.center)
		# 4. add a mask
		self.mask = pygame.mask.from_surace(self.image)

	def update(self):
		self.pos += self.direction * self.speed * dt
		self.rect.topleft = (round(self.pos.x) , round(self.pos.y))

		# MEMORY efficiency
		if self.rect.top > WINDOW_HEIGHT:
			self.kill()
class Score:
	def __init__(self):
		self.font = pygame.font.Font("./subatomic.ttf", 50)
	
	def display(self):

		score_text = f'Score: {pygame.time.get_ticks() // 1000}'
		text_surf = self.font.render(score_text, True, (255,255,255))
		text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2 , WINDOW_HEIGHT - 80))
		display_surface.blit(text_surf, text_rect)
		pygame.draw.rect(
			display_surface, 
			(255,255,255), 
			text_rect.inflate(30,30), 
			width = 8 ,
			 border_radius = 4)
	

# basic setup
pygame.init()
WINDOW_WIDTH , WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
# use method to change title of the window
pygame.display.set_caption("Space Shootter")
clock = pygame.time.Clock()

# background
background_surf = pygame.image.load("../AsteriodGame/background.png").convert()

# sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)
#laser = Laser((100,300), laser_group)

# timer
meteor_time = pygame.event.custom_type()
pygame.time.set_timer(meteor_time, 400)

score = Score()

bg_music = pygame.mixer.Sound("./sounds/music.wav")
bg_music.play(loops = -1)

while True:

	#event loop
	 for event in pygame.event.get():
	 	if event.type == pygame.QUIT:
	 		pygame.quit()
	 		sys.exit()

	 	if event.type == meteor_time:
	 		meteor_y_pos = randint(-150, -50)
	 		meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
	 		Meteor((meteor_x_pos, meteor_y_pos), groups = meteor_group)

	 # framerate limit
	 dt = clock.tick(120) / 1000 # 12 millisecs

	 # background
	 display_surface.blit(background_surf, (0,0))

	 # update
	 spaceship_group.update()
	 laser_group.update()
	 meteor_group.update()

	 # score
	 score.display()

	 # graphics
	 spaceship_group.draw(display_surface)
	 laser_group.draw(display_surface)
	 meteor_group.draw(display_surface)

	 # draw the frame
	 pygame.display.update()
