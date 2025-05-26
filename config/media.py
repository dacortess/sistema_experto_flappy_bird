import pygame, os

# Init mixer and pygame for sounds and fonts

pygame.mixer.init()
pygame.init()

# Window Images

window_img = {
    'background': pygame.image.load(os.path.join('.\\assets', 'images', 'background.png')),
    'icon': pygame.image.load(os.path.join('.\\assets', 'images', 'icon.png'))
}

# object Images

objects_img = {
    'ground': pygame.image.load(os.path.join('.\\assets', 'images', 'ground.png')),
    'top_pipe': pygame.image.load(os.path.join('.\\assets', 'images', 'pipe_top.png')),
    'bottom_pipe': pygame.image.load(os.path.join('.\\assets', 'images', 'pipe_bottom.png'))
}

# Messages Images

messages_img = {
    
    'game_over': pygame.image.load(os.path.join('.\\assets', 'images', 'game_over.png')),
    'start': pygame.image.load(os.path.join('.\\assets', 'images', 'start.png'))
}

# Player Images

player_img = [
    pygame.image.load(os.path.join('.\\assets', 'images', 'bird_down.png')),
    pygame.image.load(os.path.join('.\\assets', 'images', 'bird_mid.png')),
    pygame.image.load(os.path.join('.\\assets', 'images', 'bird_up.png'))
]

# Sounds Init

die = pygame.mixer.Sound(os.path.join('.\\assets', 'sounds', 'die.wav'))
flap =  pygame.mixer.Sound(os.path.join('.\\assets', 'sounds', 'flap.wav'))
hit = pygame.mixer.Sound(os.path.join('.\\assets', 'sounds', 'hit.wav'))
point = pygame.mixer.Sound(os.path.join('.\\assets', 'sounds', 'point.wav'))

# Game Sounds

sfx = {
    'die': die,
    'flap': flap,
    'hit': hit,
    'point': point
}

# Score Font

font = pygame.font.SysFont('Segoe', 26)

