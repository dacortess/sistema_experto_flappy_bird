import pygame
from config.media import window_img

class Window():
    """
    A class that control how window works

    ...

    Attributes
    ----------
    width : int
        Window width
    height : int
        Window height
    caption : str
        Window caption
    fps : int
        Frame per second
    background : pygame.Surface
        A surface that is used as background
    window : pygame.display
        Window object by pygame

    """

    def __init__(self) -> None:
        self.width: int = 551
        self.height: int = 720
        self.caption: str = "Flappy Bird"
        self.fps: int = 60
        self.background = self.set_background()
        self.window = pygame.display.set_mode((self.width, self.height))

    def start(self) -> None:
        """
        Set game caption and icon

            Args:
                None
            Returns:
                icon (pygame.display) : Icon Object
        """
        pygame.display.set_caption(self.caption)
        icon = pygame.display.set_icon(window_img['icon'])
        return icon

    
    def set_background(self) -> None:
        """
        Set game background

            Args:
                None
            Returns:
                bg (pygame.transform) : Final background
        """
        bg = pygame.transform.rotate(pygame.transform.scale(
        window_img['background'], (551, 720)), 0)

        return bg
    
    def blit(self, object, coordinates):
        """
        Blit window with and object

            Args:
                None
            Returns:
                None
        """
        self.window.blit(object, coordinates)