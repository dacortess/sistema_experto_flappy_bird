# Pygame
import pygame
import neat

# System
from sys import exit
import random

# Gamedata
from config.window import Window
from logic.objects import Pipe
from logic.objects import Ground
from logic.objects import Player
from logic.objects import Score
from config.variables import window_dimensions as win_dim
from config.variables import ground_position as pos_ground
from config.media import objects_img
from config.media import player_img
from config.media import messages_img
from config.media import sfx
from config.media import font

pygame.init()

class Train():
    """
    A class that control the game logic

    ...

    Attributes
    ----------
    clock : pygame.time.Clock
        Game framerate
    window : Window
        A class that controls all the window settings
    score : Score
        A class that controls the score
    player: pygame.sprite.GroupSingle
        Sprite system for player settings
    ground: pygame.sprite.Group
        Sprite system for ground settings
    pipes: pygame.sprite.Group
        Sprite system for pipes settings
    game_status: bool
        Represents if the game is finished or not
    die_sounds: bool
        Control of die sound
    hit_sounds: bool
        Control of hit sound

    """
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.window: Window = Window()
        self.score: Score = Score()
        self.players = []
        self.ground = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.game_status: True = True
        self.die_sound: True = True
        self.hit_sound: True = True
    
    def reset_game(self) -> None:
        """
        Restart all the class variables

            Args:
                None
            Returns:
                None
        """
        
        self.score = Score()
        self.player = pygame.sprite.GroupSingle()
        self.ground = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.game_status: True = True
        self.die_sound: True = True
        self.hit_sound: True = True

    def check_quit(self) -> None:
        """
        Check if the player quit the game

            Args:
                None
            Returns:
                None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    def eval_genomes(self, genomes, config) -> None:
        """
        Menu and play again loop and logic

            Args:
                None
            Returns:
                None
        """

        while self.game_status:

            # Window Config

            self.window.start()

            # Check Quit

            self.check_quit()

            # Set Background

            self.window.window.fill((0,0,0))
            self.window.blit(self.window.background, (0,0))
            self.window.blit(objects_img['ground'], (0, 520))
            self.window.blit(player_img[1], (100,250))
            
            # User Input
            
            self.train_loop(genomes, config)

            self.reset_game()
            
            pygame.display.update()


    def train_loop(self, genomes, config) -> None:
        """
        Game loop that controls all window draws and blits

            Args:
                None
            Returns:
                None
        """

        # Initialize Objects
        nets=[]
        ge=[]

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            player_class = pygame.sprite.GroupSingle()
            player_class.append(Player())
            self.player.append(player_class)
            ge.append(genome)
        
        self.ground.add(Ground(pos_ground[0], pos_ground[1]))
        pipe_timer: int = 0

        run: bool = True

        while run:

            # Check Quit

            self.check_quit()

            # Set Background

            self.window.blit(self.window.background, (0,0))

            # Check User Input

            user_input = pygame.key.get_pressed()

            # Draw Objects
            for player in self.players:
                self.player.draw(self.window.window)
            self.ground.draw(self.window.window)
            self.pipes.draw(self.window.window)

            # Spawn Ground

            if len(self.ground) <= 2:
                self.ground.add(Ground(win_dim[0], pos_ground[1]))

            # Show Score

            score_tect = font.render(f'Score: {self.score.score}', True, pygame.Color(255, 255, 255))
            self.window.blit(score_tect, (20, 20))

            # Update Objects
            for player in self.players:
                if self.player.sprite.alive:
                    self.pipes.update(self.score, ge=ge)
                    self.ground.update()
                self.player.update(user_input)

            # Collisions
            for i, player in enumerate(self.players):
                collision_pipes = pygame.sprite.spritecollide(self.player.sprites()[0], self.pipes, False)
                collision_ground = pygame.sprite.spritecollide(self.player.sprites()[0], self.ground, False)
                if collision_pipes or collision_ground:
                    if collision_pipes:
                        if self.hit_sound:
                            sfx['hit'].play()
                            self.hit_sound = False
                    self.player.sprite.alive = False
                    if collision_ground:
                        if self.die_sound:
                            sfx['die'].play()
                            self.die_sound = False
                    ge[i].fitness -= 1
                    self.players.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                                                       
                # Game Restart

                if user_input[pygame.K_r]:
                    self.score.score = 0
                    self.game_status = False
                    break

            # Spawn Pipes

            if pipe_timer <= 0 and self.player.sprite.alive:
                x_top, x_bottom = 550, 550
                y_top = random.randint(-600,-480)
                y_bottom = y_top + random.randint(90, 130) + objects_img['bottom_pipe'].get_height()
                self.pipes.add(Pipe(x_top, y_top, objects_img['top_pipe'], 'top'))
                self.pipes.add(Pipe(x_bottom, y_bottom, objects_img['bottom_pipe'], 'bottom'))
                pipe_timer = random.randint(180, 250)
            pipe_timer: int = pipe_timer - 1

            # Pygame config

            self.clock.tick(60)
            pygame.display.update()