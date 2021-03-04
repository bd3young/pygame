import sys
import pygame
from time import sleep
from settings import Settings
from gameStats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


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

        # creat an instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.createFleet()

        # make play button
        self.playButton = Button(self, "play")

        # Set the background color.
        self.bgColor = (0, 230, 0)

    def runGame(self):
        """Start the main loop for the game."""
        while True:
            self.checkEvents()

            if self.stats.gameActive:
                self.ship.update()
                self.updateBullets()
                self.updateAliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                self.checkPlayButton(mousePos)

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

    def checkPlayButton(self, mousePos):
        """Start a new game when the player clicks Play."""
        buttonClicked = self.playButton.rect.collidepoint(mousePos)
        if buttonClicked and not self.stats.gameActive:
            #reset the game stats
            self.settings.initializeDynamicSettings()
            self.stats.resetStats()
            self.stats.gameActive = True
            self.sb.prepScore()
            self.sb.prepLevel()
            self.sb.prepShips()

            #get rid of any rmaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #creat new fleet and center ship
            self.createFleet()
            self.ship.centerShip()

            # hide mouse cursor
            pygame.mouse.set_visible(False)

    def shipHit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.shipsLeft > 0:
            # Decrement ships_left.
            self.stats.shipsLeft -= 1
            self.sb.prepShips()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self.createFleet()
            self.ship.centerShip()

            # Pause.
            sleep(0.5)
        else:
            self.stats.gameActive = False
            pygame.mouse.set_visible(True)
        

    def createFleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alienWidth, alienHeight = alien.rect.size
        availableSpaceX = self.settings.screenWidth - (2 * alienWidth)
        numberAliensX = availableSpaceX // (2 * alienWidth)

        # Determine the number of alien rows
        shipHeight = self.ship.rect.height
        availableSpaceY = (self.settings.screenHeight - (3 * alienHeight) - shipHeight)
        numberRows = availableSpaceY // (2 * alienHeight)

        # Create full fleet of aliens.
        for rowNumber in range(numberRows):
            for alienNumber in range(numberAliensX):
                self.createAlien(alienNumber, rowNumber)

    def createAlien(self, alienNumber, rowNumber):
        alien = Alien(self)
        alienWidth, alienHeight = alien.rect.size
        alien.x = alienWidth + 2 * alienWidth * alienNumber
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * rowNumber
        self.aliens.add(alien)

    def updateAliens(self):
        """ Update positon of all aliens """
        self.checkFleetEdges()
        self.aliens.update()

        # look for alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.shipHit()

        # look for aliens hitting bottom
        self.checkAliensBottom()

    def checkFleetEdges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.checkEdges():
                self.changeFleetDirection()
                break

    def changeFleetDirection(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleetDropSpeed
        self.settings.fleetDirection *= -1

    def checkAliensBottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self.shipHit()
                break

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

        self.checkBulletAlienCollisions()

    def checkBulletAlienCollisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alienPoints * len(aliens)
            self.sb.prepScore()
            self.sb.checkHighScore()

        if not self.aliens:
            #destroy exisiting bullets and create new fleet
            self.bullets.empty()
            self.createFleet()
            self.settings.increaseSpeed()

            # Increase level
            self.stats.level += 1
            self.sb.prepLevel()

    def updateScreen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bgColor)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.drawBullet()
        self.aliens.draw(self.screen)

        #draw score info
        self.sb.showScore()

        # draw the play button if the game is inactive.
        if not self.stats.gameActive:
            self.playButton.drawButton()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.runGame()