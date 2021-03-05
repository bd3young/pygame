import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the jet"""
    def __init__(self, ai_game):
        """Create a bullet object at the jet's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bulletColor
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bulletWidth, self.settings.bulletHeight)
        self.rect.midtop = ai_game.jet.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bulletSpeed
        # Update the rect position.
        self.rect.y = self.y

    def drawBullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)