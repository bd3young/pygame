import pygame
from pygame.sprite import Sprite
class Plane(Sprite):
    """A class to represent a single plane in the fleet."""
    def __init__(self, ai_game):
        """Initialize the plane and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the plane image and set its rect attribute.
        image = pygame.image.load('images/enemyPlane.png')
        self.image = pygame.transform.scale(image, (70, 60))
        self.rect = self.image.get_rect()

        # Start each new plane near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the plane's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """ Move the plane to the right """
        self.x += (self.settings.planeSpeed * self.settings.fleetDirection)
        self.rect.x = self.x

    def checkEdges(self):
        """ Return true if plane is at edge """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True