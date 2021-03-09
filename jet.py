import pygame
from pygame.sprite import Sprite

class Jet(Sprite):
    """A class to manage the Jet."""
    def __init__(self, ai_game):
        """Initialize the Jet and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the jet image and get its rect.
        image = pygame.image.load('images/fighterJet.png')
        self.image = pygame.transform.scale(image, (60, 60))
        self.changeImageSize = pygame.transform.scale(self.image, (100,100) )
        self.rect = self.image.get_rect()

        # Start each new jet at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the jet's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.movingRight = False
        self.movingLeft = False

    def update(self):
        """ update jets position on move flag """
        # Update the jet's x value, not the rect.
        if self.movingRight and self.rect.right < self.screen_rect.right:
            self.x += self.settings.jetSpeed
        elif self.movingLeft and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.jetSpeed
        
        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the jet at its current location."""
        self.screen.blit(self.image, self.rect)

    def centerJet(self):
        """Center the jet on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)