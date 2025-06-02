import pygame
import random

from config.media import objects_img, player_img, sfx

from config.variables import window_dimensions as dimensios
from config.variables import scroll_speed
from config.variables import bird_position as start_position

class Ground(pygame.sprite.Sprite):
    """
    A class that control how Ground works

    ...

    Attributes
    ----------
    image : 
        Ground image
    rect : 
        Image rectangle
    """
     
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = objects_img['ground'] # Select Ground img
        self.rect = self.image.get_rect() # Create rectangle from img
        self.rect.x, self.rect.y = x, y # Set coordinates of Ground

    def update(self) -> None:
        """
        Update ground object

            Args:
                None
            Returns:
                None
        """
        # Move Ground

        self.rect.x -= scroll_speed
        if self.rect.x <= -dimensios[0]:
            self.kill()

class Player(pygame.sprite.Sprite):
    """
    A class that control how Player works

    ...

    Attributes
    ----------
    image : 
        Ground image
    rect : 
        Image rectangle
    image_index : int
        Control the player sprite system
    vel : int
        Player velocity
    flap : bool
        Control player flap
    alive : bool

    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img[0] # Select Player img
        self.rect = self.image.get_rect() # Create rectangle from img
        self.rect.center = start_position # Set coordinates of Player
        self.image_index: int  = 0 # Set rotation of Player
        self.vel: int = 0 # Set velocity of Player
        self.flap: bool = False # Set flap of Player
        self.alive: bool = True # Set state of Player
    
    def update(self, user_input, train= False) -> None:
        """
        Update player object

            Args:
                None
            Returns:
                None
        """
        #Animate bird

        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = player_img[self.image_index // 10]

        # Player movement

        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Player sprites

        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            sfx['flap'].play()
            self.flap = True
            self.vel = -7

    def jump(self) : 
        if not self.flap and self.rect.y > 0 and self.alive:
            sfx['flap'].play()
            self.flap = True
            self.vel = -7

    def move(self) : 

        #Animate bird

        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = player_img[self.image_index // 10]

        # Player movement

        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Player sprites

        self.image = pygame.transform.rotate(self.image, self.vel * -7)

class Pipe(pygame.sprite.Sprite):
    """
    A class that control how Pipe works

    ...

    Attributes
    ----------
    image : 
        Ground image
    rect : 
        Image rectangle
    enter : bool
        Check if player enter the pipe
    exit : bool
        Check if player exit the pipe
    passed : bool
        Check if player is passing the pipe
    alive : bool
        Check if player is alive
    pipe_type : str
        Check if pipe is top or bottom
    score : int 
        Player score
    """

    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image # # Select Pipe img
        self.rect = self.image.get_rect() # Create rectangle from img
        self.rect.x, self.rect.y = x, y # Set cordinates of Pipe
        self.enter = False
        self.exit = False
        self.passed = False
        self.pipe_type: str = pipe_type
        self.score: int = 0
        self.PIPE_TOP = pygame.transform.flip(image, False, True)

    def update(self, score, ge=None) -> None:
        """
        Update Pipe object

            Args:
                score (Score): Player score object
            Returns:
                None
        """

        self.rect.x -= scroll_speed
        if self.rect.x <= -dimensios[0]:
            self.kill()

        # Score

        if self.pipe_type == 'bottom':
            if start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                sfx['point'].play()
                score.update()
                if ge is not None:
                    for g in ge:
                        g.fitness += 5
    
    def get_score(self):
        return self.score

class Score():
    """
    A class that control how Score works

    ...

    Attributes
    ----------
    None
    """
    def __init__(self) -> None:
        self.score = 0
    
    def update(self) -> None:
        """
        Update score

            Args:
                None
            Returns:
                None
        """
        self.score += 1
