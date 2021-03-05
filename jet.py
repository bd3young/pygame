import pygame
from pygame.sprite import Sprite

class Jet(Sprite):
    """A class to manage the ship."""
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/fighterJet.png')
        self.changeImageSize = pygame.transform.scale(self.image, (100,100) )
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.movingRight = False
        self.movingLeft = False

    def update(self):
        """ update ships position on move flag """
        # Update the ship's x value, not the rect.
        if self.movingRight and self.rect.right < self.screen_rect.right:
            self.x += self.settings.shipSpeed
        elif self.movingLeft and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.shipSpeed
        
        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def centerShip(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)