import pygame
import os
import random
import sys

pygame.init()

# Global Constants
Screen_Width = 1100
Screen_Height = 600
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

Running =   [pygame.image.load(os.path.join("Textures/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Textures/Dino", "DinoRun2.png"))]
Jumping = pygame.image.load(os.path.join("Textures/Dino", "DinoJump.png"))
Bending = [pygame.image.load(os.path.join("Textures/Dino", "DinoBend1.png")),
           pygame.image.load(os.path.join("Textures/Dino", "DinoBend2.png"))]
Small_Cactus = [pygame.image.load(os.path.join("Textures/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "SmallCactus3.png"))]
Large_Cactus = [pygame.image.load(os.path.join("Textures/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "LargeCactus3.png"))]

Bird = [pygame.image.load(os.path.join("Textures/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Textures/Bird", "Bird2.png"))]

Cloud = pygame.image.load(os.path.join("Textures/Other", "Cloud.png"))

Background = pygame.image.load(os.path.join("Textures/Other", "BackGround.png"))

class Dinosaur:
    X_Position = 80
    Y_Position = 310
    Jump_Velocity = 8.5 # The larger this Value, the higher it jumps.
    Y_Position_Bend = 340

    def __init__(self):
        self.run_image = Running
        self.jump_image = Jumping
        self.bend_image = Bending

        self.dino_run = True
        self.dino_jump = False
        self.dino_bend = False

        self.step_index = 0 # We will use it for animation.
        self.jump_velocity = self.Jump_Velocity
        self.image = self.run_image[0] # It starts from the first picture.
        self.dino_rect = self.image.get_rect() # Collider
        self.dino_rect.x = self.X_Position
        self.dino_rect.y = self.Y_Position

    def update(self, userInput):
        if self.dino_run:
                self.run()
        if self.dino_jump:
                self.jump()
        if self.dino_bend:
                self.bend()

        if self.step_index >= 10:
                self.step_index = 0
            
        if userInput[pygame.K_SPACE] or userInput[pygame.K_UP] and not self.dino_jump:
                self.dino_run = False
                self.dino_jump = True
                self.dino_bend = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
                self.dino_run = False
                self.dino_jump = False
                self.dino_bend = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_run = True
                self.dino_jump = False
                self.dino_bend = False

    def run(self):
        self.image = self.run_image[self.step_index // 5] # The dinosaur changes its image every 5 frames.
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_Position
        self.dino_rect.y = self.Y_Position
        self.step_index += 1

    def jump(self):
        self.image = self.jump_image
        if self.dino_jump:
              self.dino_rect.y -= self.jump_velocity * 4 # Used to visually adjust the height/speed of the jump.
              self.jump_velocity -= 0.8 # Gravity
        if self.jump_velocity < -self.Jump_Velocity: # When the falling speed reaches the negative of the initial jump speed (i.e. equal downward value), the dinosaur is considered to have landed again.
              self.dino_jump = False
              self.jump_velocity = self.Jump_Velocity


    def bend(self):
          self.image = self.bend_image[self.step_index // 5]
          self.dino_rect = self.image.get_rect()
          self.dino_rect.x = self.X_Position
          self.dino_rect.y = self.Y_Position_Bend
          self.step_index += 1

    def draw(self, Screen):
        Screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y)) # This function provide draw dinosaurs.

class Clouds:
      def __init__(self):
            self.x = Screen_Width + random.randint(800, 1000)
            self.y = random.randint(50, 100) # This ensures that the clouds are not aligned.
            self.image = Cloud
            self.width = self.image.get_width()
            
      def update(self):
            self.x -= game_Speed
            if self.x < -self.width: # If the cloud moves completely from the left of the screen.
                  self.x = Screen_Width + random.randint(2500, 3000)
                  self.y = random.randint(50, 100)
            
      def draw(self, Screen):
            Screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        # Collider is created here.
        self.rect = self.image[self.type].get_rect()
        self.rect.x = Screen_Width

    def update(self):
        self.rect.x -= game_Speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
      
    def draw(self, Screen):
        Screen.blit(self.image[self.type], (self.rect))

class SmallCactus(Obstacle):
      def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
      def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
      
class Birds(Obstacle):
      def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)

        self.rect.y = 250
        self.index = 0

      def draw (self, Screen):
            if self.index >= 9:
                  self.index = 0     
            Screen.blit(self.image[self.index // 5], self.rect)
            self.index += 1
                 
def eval_genomes(genomes, config):
    # NEAT is invoked for each generation.
    global game_Speed, x_Position_Background, y_Position_Background, Points, obstacles

    # Resets the game for each generation.
    game_Speed = 14
    x_Position_Background = 0
    y_Position_Background = 380
    Points = 0
    obstacles = []

    nets = []   # Neural network for each dinosaur.
    ge = []     # Where we record the dinosaur's performance score.
    dinos = []  # The dinosaur objects that appear on screen.

    for genome_id, genome in genomes:
        genome.fitness = 0  # beginning points.
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
        dinos.append(Dinosaur())

    clock = pygame.time.Clock()
    clouds = Clouds()
    font = pygame.font.Font('freesansbold.ttf', 24)
def main ():
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    clouds = Clouds()
    global game_Speed, x_Position_Background, y_Position_Background, Points, obstacles
    game_Speed = 14
    x_Position_Background = 0
    y_Position_Background = 380
    Points = 0
    font = pygame.font.Font('freesansbold.ttf', 24) # Font
    obstacles = []
    death_Count = 0
    game_Over = False

    def Score():
          global Points, game_Speed
          Points += 1
          if Points % 100 == 0:
                game_Speed += 1

          text = font.render("Points: " + str(Points), True, (0, 0, 0)) # Black Clour.
          textRect = text.get_rect()
          textRect.center = (1000, 40)
          Screen.blit(text, textRect)

    def BackGround():
          global x_Position_Background, y_Position_Background
          image_Width = Background.get_width()
          Screen.blit(Background, (x_Position_Background, y_Position_Background)) # Draws at the current location of the background.
          Screen.blit(Background, (image_Width + x_Position_Background, y_Position_Background)) # Draws a copy of the background just to the right.
          if x_Position_Background <= -image_Width:
                Screen.blit(Background, (image_Width + x_Position_Background, y_Position_Background))
                x_Position_Background = 0
          x_Position_Background -= game_Speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        Screen.fill((255, 255, 255)) # White colour.
        userInput = pygame.key.get_pressed()

        player.update(userInput)
        player.draw(Screen)

        if len (obstacles) == 0:
              if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(Small_Cactus))
              elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(Large_Cactus))
              else:
                    obstacles.append(Birds(Bird))
      
        for Obstacle in obstacles:
              Obstacle.update()
              Obstacle.draw(Screen)
              if player.dino_rect.colliderect(Obstacle.rect):
                    death_Count += 1
                    menu(death_Count)
                    

        BackGround()

        clouds.draw(Screen)
        clouds.update()

        Score()

        clock.tick(30) # 30 frame / fps.
        pygame.display.update()

def menu(death_Count):
      global Points
      run = True
      while run:
            Screen.fill((255, 255, 255)) # White colour.

            if death_Count == 0:
                  main()
                  return
            elif death_Count > 0:
                  pass

            for event in pygame.event.get():
                  if event.type == pygame.QUIT: # This line detects when the player presses the “X” button in the game window.
                        run = False
                        pygame.quit()
                        quit()
                        sys.exit() # This line provides completely close the game. 
                  if event.type == pygame.KEYDOWN:
                        main()


menu(death_Count = 0)
