import pygame
import random
import sys


pygame.init() #initializes the pygame module

screen_width=1000
screen_height=500

score=0
player_lives=3
font=pygame.font.Font(None,36)
game_over_font=pygame.font.Font(None,64)

background_image=pygame.image.load("assets/background.png") #stores image in a given variable
background_image=pygame.transform.scale(background_image,(screen_width,screen_height)) #Tranforms the image into specified scales

screen=pygame.display.set_mode((screen_width,screen_height)) #Make variable for the game screen that has the assigned values of screen width and height
bg_x=0
speed_increase_rate=0
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Realm Quest") #The Window Box Name for the game display

enemies=[]
player_bullets=[]

class Character:
     def __init__(self,x,y): #defined the class character and enables it to call itself by using __init__ called a constructor
        self.x=x
        self.y=y
        self.img=pygame.image.load("assets/player1.png")
        self.img=pygame.transform.scale(self.img,(100,100)) #transforms image into a spcified smaller scale
        self.rect=self.img.get_rect() #creating a rectangle that is the same size as the image
        self.rect.center = (x,y)
        self.run_animation_count=0
        self.img_list=["assets/player1.png","assets/player2.png","assets/player3.png","assets/player4.png"] #this makes a list of all the images that will be used in the animation 
        self.is_jump=False
        self.jump_count=15 # makes the player go up 15 times and go back down 15 times while in a loop
        self.bullet_img='assets/bullet.png'
     def draw(self):
        self.rect.center=(self.x,self.y) #to make it certain that the values assigned to self.x and self.y are same
        screen.blit(self.img,self.rect) #used for calling that image
     
     def run_animation_player(self):
         if(not self.is_jump):
             self.img=pygame.image.load(self.img_list[int(self.run_animation_count)]) #this code runs the code iterating through al the images in the image list
             self.img=pygame.transform.scale(self.img, (100,100))
             self.run_animation_count+=0.4
             self.run_animation_count=self.run_animation_count%4

     def jump(self):
         if(self.jump_count>-15):
             n=1 # when player is going up
             if(self.jump_count<0):
                 n=-1 #when player is going down
             self.y-=((self.jump_count**2)/10)*n #indicating that player will go up adn thend own lika a parabola
             self.jump_count-=1 
         else:
             self.is_jump=False #called when jump count is equal to -15 resulting in player not to jump
             self.jump_count=15
             self.y=392 # indicating player is going back to the base ground y coordinate

     def shoot(self):
         bullet=Bullet(self.x+5,self.y-18,self.bullet_img)
         player_bullets.append(bullet)

class Enemy:
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("assets/enemy1.png")
        self.img = pygame.transform.scale(self.img , (75,75))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.run_animation_count = 0
        self.img_list1= ["assets/enemy1.png","assets/enemy2.png","assets/enemy3.png"]

    def draw(self):
        self.rect.center = (self.x,self.y)
        screen.blit(self.img,self.rect)

    def run_animation_enemy(self):
            self.img  = pygame.image.load(self.img_list1[int(self.run_animation_count)])
            self.img = pygame.transform.scale(self.img , (75,75))
            self.run_animation_count+=0.5
            self.run_animation_count = self.run_animation_count%3
            
class Bullet:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=pygame.image.load(img)
        self.img=pygame.transform.scale(self.img,(15,15))
        self.rect=self.img.get_rect()
        self.rect.center=(x,y)
    def draw(self):
        self.rect.center=(self.x,self.y)
        screen.blit(self.img,self.rect)
    def move(self,vel): #defining moving bullets velocity
        self.x+=vel
    def off_screen(self):
        return(self.x<=0 or self.x>= screen_width)

player=Character(100,392) #used to pass the function that was defined for the class Character
running = True #Game is running indication
clock=pygame.time.Clock() #Any time related functions are used with help of this function
last_enemy_spawn_time=pygame.time.get_ticks()

while running:
    score+=0.2
    for event in pygame.event.get(): #returns all events from user end
         if event.type==pygame.QUIT: #checking if user is quitting the game or not
             running=False #Game is not running
         if event.type==pygame.KEYDOWN: #checks if any key is being pressed
             if event.key==pygame.K_SPACE: #indicates which key is used for jumping
                 player.is_jump=True
             if event.key==pygame.K_TAB: #indicates whihc key is used for shooting
                 player.shoot() 
    bg_x-=(10+speed_increase_rate) #move background faster
    speed_increase_rate+=0.006
    if bg_x<=-screen_width:
         bg_x=0 #resets the loop to an infinte loop as sson as bg_x is equal to screen width    
    screen.blit(background_image,(bg_x,0)) #Print statemetn for the images in a loop
    screen.blit(background_image,(screen_width+bg_x,0)) #stops the bg from crashing and looping properly after reachign screen width value
    
    current_time=pygame.time.get_ticks()
    if current_time-last_enemy_spawn_time >=3000: # this indicates the time of enemy spawning
        if random.randint(0,100)<3: #wont spawn enemies at random places thus repeating the position
            enemy_x=screen_width+900 #location of x coordinate for enemy
            enemy_y=396 # y coordinate is same here for the enemy
            enemy=Enemy(enemy_x,enemy_y) #defining Enemy class with values assigned to it
            enemies.append(enemy) # adding to the enemy list
            last_enemy_spawn_time = current_time

    for enemy in enemies:
        enemy.x -=(15 + speed_increase_rate)
        enemy.draw()
        enemy.run_animation_enemy()           

        #Collisions 1
        if enemy.rect.colliderect(player.rect):
            speed_increasing_rate=0
            player_lives-=1
            enemies.remove(enemy)

        #Collisions 2
        for bullet in player_bullets:
            if pygame.Rect.colliderect(enemy.rect,bullet.rect):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                score+=10

    for bullet in player_bullets:
        if(bullet.off_screen()):
            player_bullets.remove(bullet)
        else:
            bullet.draw()
            bullet.move(10)

    if player_lives<=0:
        game_over_text=font.render(f"Game Over",True,(255,255,255))
        screen.blit(game_over_text,(screen_width//2 -120,screen_height//2))
        pygame.display.update() # code to explain what to do when game is over
        pygame.time.wait(2000) #Time given for waiting
        pygame.quit # end the game
        sys.exit()

    #Display
    live_text=font.render(f"Lives:{player_lives}",True,(0,0,0))
    screen.blit(live_text,(screen_width-120,10)) #diplaying lives text
    score_text=font.render(f"Score:{score//1}",True,(0,0,0))
    screen.blit(score_text,(20,10)) #diplaying score

    if(player.is_jump):
        player.jump() #if condition is true then the jump function is called
    player.draw() #Draw the character and run it in the code
    player.run_animation_player() #calling the animation function 
    pygame.display.update() #for updates in game
    clock.tick(30) #indicating the code will run only 30 times or fps indication

pygame.quit()