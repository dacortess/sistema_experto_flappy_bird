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
        self.players = pygame.sprite.Group()
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
        Evalúa una generación de genomas.

            Args:
                None
            Returns:
                None
        """

        self.game_status = True  # Reinicia el estado por si acaso
        self.train_loop(genomes, config)
        self.reset_game()

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
        players_list = []  
        pipes_list = []   

        for _, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            player = Player()
            players_list.append(player)
            self.players.add(player)
            ge.append(genome)

        self.ground.add(Ground(pos_ground[0], pos_ground[1]))
        # Initialize pipe_timer to a random value to delay the first pipe
        pipe_timer: int = 0

        run: bool = True
        pipe_ind = 0

        while run:

            # Check Quit
            self.check_quit()

            # Set Background
            self.window.blit(self.window.background, (0,0))

            # Draw Objects
            self.players.draw(self.window.window)
            self.ground.draw(self.window.window)
            self.pipes.draw(self.window.window)

            # Spawn Ground
            if len(self.ground) <= 2:
                self.ground.add(Ground(win_dim[0], pos_ground[1]))
            
            # Spawn Pipes
            if pipe_timer <= 0 and len(self.players) > 0:
                x_top, x_bottom = 550, 550
                y_top = random.randint(-600,-480)
                y_bottom = y_top + random.randint(90, 130) + objects_img['bottom_pipe'].get_height()
                pipe_top = Pipe(x_top, y_top, objects_img['top_pipe'], 'top')       # MODIFICADO
                pipe_bottom = Pipe(x_bottom, y_bottom, objects_img['bottom_pipe'], 'bottom')  # MODIFICADO
                self.pipes.add(pipe_top)  # MODIFICADO
                self.pipes.add(pipe_bottom)
                pipes_list.extend([pipe_top, pipe_bottom])  # MODIFICADO
                pipe_timer = random.randint(180, 250)
            pipe_timer: int = pipe_timer - 1

            # Show Score
            score_tect = font.render(f'Score: {self.score.score}', True, pygame.Color(255, 255, 255))
            self.window.blit(score_tect, (20, 20))

            # Update Objects
            if len(self.players) > 0:
                self.pipes.update(self.score, ge=ge)
                self.ground.update()
            
            # NEAT CONFIG
            if len(players_list) > 0:
                change_pipe = False
                for _, player in enumerate(players_list):
                    if len(pipes_list) > 0 and player.rect.topleft[0] > pipes_list[pipe_ind].rect.topleft[0] + pipes_list[pipe_ind].PIPE_TOP.get_width():
                        change_pipe = True
                if change_pipe: pipe_ind += 2
            else:
                run = False
                break
            
            for x, player in enumerate(players_list):
                ge[x].fitness = 0.016
                player.move()

                output = nets[x].activate((
                    player.rect.y,
                    abs(player.rect.y - pipes_list[pipe_ind].rect.bottomleft[1]),
                    abs(player.rect.y - pipes_list[pipe_ind + 1].rect.topleft[1])
                ))
                
                if output[0] > 0.5:
                    player.jump()
                
            # Collisions
            for i, player in enumerate(players_list):
                collision_pipes = pygame.sprite.spritecollide(player, self.pipes, False)
                collision_ground = pygame.sprite.spritecollide(player, self.ground, False)
                if collision_pipes or collision_ground or player.rect.y < 0:
                    if collision_pipes:
                        if self.hit_sound:
                            sfx['hit'].play()
                            self.hit_sound = False
                        ge[i].fitness -= 3
                    #player.sprite.alive = False
                    if collision_ground or player.rect.y < 0:
                        if self.die_sound:
                            sfx['die'].play()
                            self.die_sound = False
                        ge[i].fitness -= 5

                    self.players.remove(player)
                    players_list.pop(i)
                    nets.pop(i)
                    ge.pop(i)

            # Pygame config
            self.clock.tick(60)
            pygame.display.update()



