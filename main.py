import pygame
import random
from sys import exit

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
    self.player_walk = [player_walk1, player_walk2]
    self.player_index = 0
    self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

    self.image = self.player_walk[self.player_index]
    self.rect = self.image.get_rect(midbottom=(80, 300))
    self.gravity = 0

  def player_input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
      self.gravity = -20
      jump_sound()

  def apply_gravity(self):
    self.gravity += 1
    self.rect.y += self.gravity
    if self.rect.bottom >= 300:
      self.rect.bottom = 300

  def animation_state(self):
      if self.rect.bottom < 300:
        self.image = self.player_jump
      else:
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk): self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

  def update(self):
    self.player_input()
    self.apply_gravity()
    self.animation_state()

class Obstacle(pygame.sprite.Sprite):
  def __init__(self, type):
    super().__init__()

    if type == 'fly':
      fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
      fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
      self.frames = [fly_frame_1, fly_frame_2]
      y_pos = 210

    else:
      snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
      snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
      self.frames = [snail_frame_1, snail_frame_2]
      y_pos = 300

    self.animation_index = 0
    self.image = self.frames[self.animation_index]
    self.rect = self.image.get_rect(
        midbottom=(random.randint(900, 1100), y_pos))

  def animation_state(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames): self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]

  def update(self):
    self.animation_state()
    self.rect.x -= 6
    self.destroy()

  def destroy(self):
    if self.rect.x <= -100:
      self.kill()

def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_surf = score_font.render(f'Score: {current_time}', False, text_color)
  score_rect = score_surf.get_rect(center=(400, 50))
  screen.blit(score_surf, score_rect)
  return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

def bgmusic():
  mixer.music.load("sounds/music.mp3")
  mixer.music.set_volume(0.7)
  mixer.music.play(-1)

def jump_sound():
  jumpsound = mixer.Sound("sounds/jump.mp3")
  jumpsound.set_volume(0.4)
  mixer.Sound.play(jumpsound)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('skii spel')
clock = pygame.time.Clock()
score_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
go_font = pygame.font.Font('fonts/Pixeltype.ttf', 100)
game_active = False
start_time = 0
score = 0
obstacle_rect_list = []
text_color = (64, 64, 64)
box_color = "#c0e8ec"
mixer = pygame.mixer
mixer.init()
bgmusic()

# Surfaces
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Intro Text
introtitle_surf = go_font.render('GAME OF SKIII', False, text_color)
introtitle_rect = introtitle_surf.get_rect(center=(400, 85))

# Start-up intro text
introtext_surf = score_font.render('Press space to start', False, text_color)
introtext_rect = introtext_surf.get_rect(center=(400, 315))

# Game Over Text
go_surf = go_font.render('GAME OVER SKOOO', False, text_color)
go_rect = go_surf.get_rect(center=(400, 150))
playagain_surf = score_font.render('Press space to restart', False, text_color)
playagain_rect = playagain_surf.get_rect(center=(400, 215))

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      print("Quitting game...")
      pygame.quit()
      exit()

    if game_active:
        if event.type == obstacle_timer:
            obstacle_group.add(Obstacle(random.choice(['fly','snail','snail','snail'])))  
    else:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            start_time = int(pygame.time.get_ticks() / 1000) - start_time

  if game_active:   
    # Sky and ground surfaces
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))

    score = display_score()

    # NEW WITH CLASSES
    player.draw(screen)
    player.update()

    obstacle_group.draw(screen)
    obstacle_group.update()

    game_active = collision_sprite()

  else:
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)
    screen.blit(introtitle_surf, introtitle_rect)
    obstacle_rect_list.clear()
    player_gravity = 0

    score_message = score_font.render(f'Your score: {score}', False, text_color)
    score_message_rect = score_message.get_rect(center = (400, 330))
    
    if score == 0:
      screen.blit(introtext_surf, introtext_rect)
    else:
      screen.blit(score_message, score_message_rect)

  # Leave this
  pygame.display.update()

  # FPS-limiter 60fps
  clock.tick(60)
  