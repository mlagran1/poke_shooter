import pygame,sys,math
from pygame.locals import *
from random import randint

class Enemy(pygame.sprite.Sprite):
	def __init__(self, gs=None, ntype=None):
		pygame.sprite.Sprite.__init__(self)

		#load game state
		self.gs = gs
		self.typeN = ntype

		#other varaibles
		self.image_right = {1:"Sprites/" + self.gs.sprites[self.typeN] + "/right_move.png", -1:"Sprites/" + self.gs.sprites[self.typeN] + "/right_still.png"}
		self.image_left = {1:"Sprites/" + self.gs.sprites[self.typeN] + "/left_move.png", -1:"Sprites/" + self.gs.sprites[self.typeN] + "/left_still.png"}
		self.spot = randint(0,1)
		self.right = -1
		self.left = -1
		self.timer = 0
		self.death_count = 0
		self.health = self.typeN * 1.5
		#create image
		if self.spot == 0:
			self.image = pygame.image.load(self.image_right[self.right])
			self.rect = self.image.get_rect()
			self.rect = self.rect.move(1,510)
		else:
			self.image = pygame.image.load(self.image_left[self.left])
			self.rect = self.image.get_rect()
			self.rect = self.rect.move(799,510)

	def tick(self):
		if self.spot == 0:
			self.rect = self.rect.move(2,0)
			self.image = pygame.image.load(self.image_right[self.right])
			if self.timer % 5 == 0:
				self.right = self.right * -1
		if self.spot == 1:
			self.rect = self.rect.move(-2,0)
			self.image = pygame.image.load(self.image_left[self.left])
			if self.timer % 5 == 0:
				self.left = self.left * -1

		self.timer +=1

class Power_Up(pygame.sprite.Sprite):
	def __init__(self, gs=None, ptype=None):
		pygame.sprite.Sprite.__init__(self)

		#load game state
		self.gs = gs

		#other vairables
		self.typeP = ptype
		self.powers = ['NONE','BOMB','INCREASED BALL POWER']
		
		#create image
		if self.powers[self.typeP] != 'NONE':
			self.image = pygame.image.load("Power/"+ self.powers[self.typeP] + ".png")
			self.rect = self.image.get_rect()
			self.rect = self.rect.move(randint(100,700),0)
	
	def tick(self):
		if self.rect[1] < 510:
			self.rect = self.rect.move(0,2)
		
	def bomb(self):
		for enemy in self.gs.enemies:
			self.gs.marked_enemies.append(enemy)
			self.gs.score +=1
			
		#clear the power ups list
		self.gs.power_ups = []
	
	def increase_ball_pwr(self): 
			self.gs.increased_rate+=.5
			self.gs.power_ups = []
	

class Player(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		#load the game state
		self.gs = gs

	#creates image
		self.image = pygame.image.load("Sprites/" + self.gs.sprites[0] + '/front.png')
		self.rect = self.image.get_rect()
		self.orig_image = self.image
		self.rect = self.rect.move(320,510)

		#other variables
		self.fire = False
		self.dead_player = False
		self.power = Power_Up(self.gs,0)
		self.typeN = 0
		self.image_right = {1:"Sprites/" + self.gs.sprites[self.typeN] + "/right_move.png", -1:"Sprites/" + self.gs.sprites[self.typeN] + "/right_still.png"}
		self.image_left = {1:"Sprites/" + self.gs.sprites[self.typeN] + "/left_move.png", -1:"Sprites/" + self.gs.sprites[self.typeN] + "/left_still.png"}
		self.right_count = 1
		self.left_count = 1
		self.timer = 0
		self.power_flag = False
		#variables for jumping
		self.jump = 0
		self.jump_max = 0
		self.jump_enabled = False
		self.peak = False

	def tick(self):
		mx, my = pygame.mouse.get_pos()
		self.angle = -1*math.degrees((math.atan2(my-self.rect.center[1], mx-self.rect.center[0])+math.pi))
		self.rads = self.angle*math.pi/180

		if not self.dead_player:
			if self.fire == True and self.gs.counter % self.gs.fire_rate == 0:
				self.gs.balls.append(Balls(self.gs,self.rads,self.gs.ball_num))
				#self.fire = False
		
			#facing left
			if mx <= self.rect.center[0]:
				self.image = pygame.image.load(self.image_left[-1])
				#move person righht
				if self.gs.pressed["right"] == True:
					self.rect = self.rect.move(5,0)
					self.image = pygame.image.load(self.image_left[self.left_count])
					#changing the sprite
					if self.timer % 5 == 0:
						self.left_count = self.left_count * -1
				#move person left
				if self.gs.pressed['left'] == True:
					self.rect = self.rect.move(-5,0)
					self.image = pygame.image.load(self.image_left[self.left_count])
					#changing the sprite
					if self.timer % 5 == 0:
						self.left_count = self.left_count * -1

			#facing right
			if mx > self.rect.center[0]:
				self.image = pygame.image.load(self.image_right[-1])
				#move person righht
				if self.gs.pressed["right"] == True:
					self.rect = self.rect.move(5,0)
					self.image = pygame.image.load(self.image_right[self.right_count])
					#changing the sprite
					if self.timer % 5 == 0:
						self.right_count = self.right_count * -1
				#move person left
				if self.gs.pressed['left'] == True:
					self.rect = self.rect.move(-5,0)
					self.image = pygame.image.load(self.image_right[self.right_count])
					#changing the sprite
					if self.timer % 5 == 0:
						self.right_count = self.right_count * -1

			if self.gs.pressed["up"] == True and self.jump_enabled == False:
				self.jump_max = 15
				self.jump_enabled = True

			if self.jump < self.jump_max and self.peak == False:
				self.rect = self.rect.move(0,-5)
				self.jump+=1

				if self.jump == self.jump_max:
					self.peak = True
					self.jump_max = 0

			if self.jump >= self.jump_max and self.peak == True and self.jump != 0:
				self.rect = self.rect.move(0,5)
				self.jump-=1

			if self.jump == 0:
				self.jump_enabled = False
				self.peak = False
				self.jump_max = 0


			if self.gs.pressed['shift'] and self.power_flag == True:
				self.gs.pressed['shift'] = False
				#calls the bomb power
				if self.power.powers[self.power.typeP] == 'BOMB':
					self.power.bomb()
					self.power_flag = False
				elif self.power.powers[self.power.typeP] == 'INCREASED BALL POWER':
					self.power.increase_ball_pwr();
					self.power_flag = False
				
				#resetting the power
				self.power = Power_Up(self.gs,0)

			#increment counter
			self.timer +=1
		else:
			self.image = pygame.image.load("Sprites/" + self.gs.sprites[self.typeN] + "/splat.png")

	def player_hit(self,enemy):
		if self.rect.colliderect(enemy.rect):
			self.dead_player = True
	
	def got_power(self,power):
		if self.rect.colliderect(power.rect):
			self.power_flag = True
			self.power = power
			power.rect = power.rect.move(810,0)

class Balls(pygame.sprite.Sprite):
	def __init__(self, gs=None,rads=None,t=None):
		pygame.sprite.Sprite.__init__(self)

		#load the game staet
		self.gs = gs
		self.rads = rads
		#other variables
		self.type_count = t
		self.ball_types = {1:"balls/Masterballs/Masterball-", 2:"balls/Ultraballs/Ultraball-", 3:"balls/Greatballs/Greatball-", 4:"balls/Pokeballs/Pokeball-"}
		self.ball_pwr = {1:10+self.gs.increased_rate, 2:7+self.gs.increased_rate, 3:3+self.gs.increased_rate, 4:2+self.gs.increased_rate}

		#creating image
		self.image = pygame.image.load(self.ball_types[self.type_count] + str(20) + ".png")
		self.rect = self.gs.player.rect
	
	def move(self):
		self.rect = self.rect.move(-10*math.cos(self.rads),10*math.sin(self.rads))

	def tick(self):
		self.move()
	

class GameSpace:
	
	#removes the balls that are off screen from the list
	def off_screen_balls(self):
		temp = []
		for b in self.balls:
			if (b.rect[0] < 800 and b.rect[0] > 0):
				temp.append(b)
		self.balls = []
		self.balls = temp

	#removes enemies that are off screen from the list (hit or not)
	def off_screen_enemies(self):
		temp = []
		for e in self.enemies:
			if (e.rect[0] < 800 and e.rect[0] >0):
				temp.append(e)
		
		self.enemies = []
		self.enemies = temp

	#removes power up from screen when picekd up
	def off_screen_power(self):
		temp =[]
		for p in self.power_ups:
			if(p.rect[0] < 800 and p.rect[0] > 0):
				temp.append(p)
		self.power_ups = []
		self.power_ups = temp

	#removes hit enemies from screen
	def enemy_hit(self,ball):
		for enemy in self.enemies:
			if ball.rect.colliderect(enemy.rect) and ball not in self.marked_balls and enemy not in self.marked_enemies:
				self.marked_balls.append(ball)
				ball.rect = ball.rect.move(850,0)
				enemy.health = enemy.health - ball.ball_pwr[ball.type_count]
				if enemy.health <= 0:
					self.marked_enemies.append(enemy)
					self.score +=1

	def dead(self,enemy):
		if enemy.death_count < 35:
			enemy.image = pygame.image.load("Sprites/" + self.sprites[enemy.typeN] + "/splat.png")
			enemy.death_count +=1
		else:
			enemy.rect = enemy.rect.move(850,0)
	
	def next_level(self):
		self.level +=1
		self.max_type +=1
		self.curr_enemies = 0
		self.num_enemies +=20
		##self.enemies = []
		self.balls = []
		self.marked_enemies = []
		self.marked_balls = []
		
		if self.frequency > 20:
			self.frequency -=10

		if self.level % 3 == 0 and self.fire_rate > 5:
			self.fire_rate -=2

		if self.level == 4:
			self.ball_num = 3

		if self.level == 10:
			self.ball_num = 2

		if self.level == 25:
			self.ball_bum = 1
	

	def main(self):
		pygame.init()
		
		#screen size and background
		self.size = self.width, self.height = 800,640
		self.white = 255,255,255
		self.bg = pygame.image.load("Sprites/background.png")

		#initialize text
		self.myfont = pygame.font.SysFont("monospace",25)

		#initialize music
		self.music = {1:"Music/pallet.wav", 2:"Music/pewter.wav", 3:"Music/celadon.wav",4:"Music/center.wav", 5:"Music/cycling.wav", 6:"Music/The Pit.wav"}
		self.thugga = {1:"Music/Check.wav"}
		self.music_num = randint(1,5)

		#picks the song list
		if len(sys.argv) == 1:
			pygame.mixer.music.load(self.music[self.music_num])
		elif len(sys.argv) == 2 and sys.argv[1] == "thugga":
			print ("Check - Young Thug")
			pygame.mixer.music.load(self.thugga[1])

		pygame.mixer.music.play(-1)

		#Game screen and clock
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		#other variables
		self.score = 0	#the score
		self.level = 1	#the level
		self.max_type = 1	#the types of enemies that are allowed at the current level
		self.num_enemies = 20	#the max number of enemies allowed at the current level
		self.curr_enemies = 0	#the number of enemies that have been produced
		self.sprites = ['ash', 'arbok', 'char', 'pikachu', 'squirtle', 'diglet', 'golem', 'gastly', 'snorlax', 'cubone', 'grimer', 'eevvee', 'jigg']
		self.balls = []	#list that holds the Balls objects
		self.enemies = [] #the list that hodls the Enemy objects
		self.power_ups = []
		self.marked_enemies = [] #list that holds the hit enemies
		self.marked_balls = []	#list that holds the balls that hit enemies
		self.single_shot = 0
		self.counter = 0
		self.frequency = 90 #how often the pokemon come
		self.ball_num = 4 #the pokeball currently beigng shot
		self.fire_rate = 20
		self.power_up_out = False
		self.increased_rate = 0

		self.pressed = {"right":False, "left":False, "mouse":False, "shift":False, "up":False}
		#game objects
		self.player = Player(self)
		#starting game loop
		while 1:
			#handle user inputs
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()

				#handles keyboard pressed
				if event.type == KEYDOWN:
					if(event.key == pygame.K_d):
						self.pressed['right'] = True
					if(event.key == pygame.K_a):
						self.pressed['left'] = True
					if(event.key == pygame.K_LSHIFT):
						self.pressed['shift'] = True
					if(event.key == pygame.K_w):
						self.pressed['up'] = True

				#handles keyboard release
				if event.type == KEYUP:
					if(event.key == pygame.K_d):
						self.pressed['right'] = False
					if(event.key == pygame.K_a):
						self.pressed['left'] = False
					if (event.key == pygame.K_LSHIFT):
						self.pressed['shift'] = False
					if(event.key == pygame.K_w):
						self.pressed['up'] = False

				if event.type == MOUSEBUTTONDOWN:
					self.pressed['mouse'] = True
					self.player.fire = True
					self.single_shot +=1	

				if event.type == MOUSEBUTTONUP:
					self.pressed['mouse'] = False
					self.player.fire = False

			self.typeN = randint(1,self.max_type)

			if len(self.marked_enemies) < self.num_enemies and randint(0,self.frequency) == 0:
				self.enemies.append(Enemy(self,self.typeN))
				self.curr_enemies +=1

			#next level funtion
			if len(self.marked_enemies) == self.num_enemies and self.player.dead_player == False:
				self.next_level()
				self.power_up_out = False

			#power_ups
			if randint(0,1000) == 0 and self.power_up_out == False and self.player.power_flag == False:
				self.power_ups.append(Power_Up(self,randint(1,2)))
				self.power_up_out = True

			#clock tick
			self.clock.tick(60)
			self.player.tick()
			self.counter +=1

			#display
			self.screen.fill(self.white)
			self.screen.blit(self.bg,(0,0))

			#sound
			#sound.play(-1)

			#show enemies
			for enemy in self.enemies:
				if enemy not in self.marked_enemies:
					enemy.tick()
					self.player.player_hit(enemy)
				else:
					self.dead(enemy)

				enemy.image = pygame.transform.scale(enemy.image,(30,30))
				self.screen.blit(enemy.image, enemy.rect)
			#handles balls
			for ball in self.balls:
				ball.tick()
				self.enemy_hit(ball)
				self.screen.blit(ball.image, ball.rect)

			for power in self.power_ups:
				power.tick()
				self.player.got_power(power)
				self.screen.blit(power.image, power.rect)
		
			self.off_screen_balls()
			self.off_screen_enemies()
			self.off_screen_power()

			#player and other images
			self.player.image = pygame.transform.scale(self.player.image,(30,30))
			self.screen.blit(self.player.image, self.player.rect)

			score = self.myfont.render("SCORE: "+str(self.score),1,(255,255,255))
			level = self.myfont.render("LEVEL: "+str(self.level),1,(255,255,255))
			power = self.myfont.render("POWER UP: "+str(self.player.power.powers[self.player.power.typeP]),1,(255,255,255))
			self.screen.blit(score,(700,50))
			self.screen.blit(level,(50,50))
			self.screen.blit(power,(300,50))
			pygame.display.flip()



#main
if __name__=='__main__':
	gs = GameSpace()
	gs.main()

