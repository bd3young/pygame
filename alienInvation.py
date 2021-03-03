import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Set the background color.
        self.bgColor = (0, 230, 0)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.checkEvents()
            self.ship.update()
            self.updateBullets()
            self.updateScreen()

    def checkEvents(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.checkKeyDownEvents(event)
            elif event.type == pygame.KEYUP:
                self.checkKeyUpEvents(event)

    def checkKeyDownEvents(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.movingRight = True
        elif event.key == pygame.K_LEFT:
            self.ship.movingLeft = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fireBullet()

    def checkKeyUpEvents(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.movingRight = False 
        elif event.key == pygame.K_LEFT:
            self.ship.movingLeft = False

    def fireBullet(self):
        """ Create a new bullet and add it to the bullets """
        if len(self.bullets) < self.settings.bulletsAllowed:
            newBullet = Bullet(self)
            self.bullets.add(newBullet)  

    def updateBullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    def updateScreen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bgColor)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.drawBullet()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()