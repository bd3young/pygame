import sys
import pygame
from time import sleep
from settings import Settings
from gameStats import GameStats
from jet import Jet
from bullet import Bullet
from plane import Plane
from button import Button
from scoreboard import Scoreboard


class JetFighter:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Jet Fighter")

        # creat an instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.jet = Jet(self)
        self.bullets = pygame.sprite.Group()
        self.planes = pygame.sprite.Group()

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
                self.jet.update()
                self.updateBullets()
                self.updatePlanes()

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
            self.jet.movingRight = True
        elif event.key == pygame.K_LEFT:
            self.jet.movingLeft = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fireBullet()

    def checkKeyUpEvents(self, event):
        if event.key == pygame.K_RIGHT:
            self.jet.movingRight = False 
        elif event.key == pygame.K_LEFT:
            self.jet.movingLeft = False

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
            self.sb.prepJets()

            #get rid of any rmaining planes and bullets
            self.planes.empty()
            self.bullets.empty()

            #creat new fleet and center jet
            self.createFleet()
            self.jet.centerJet()

            # hide mouse cursor
            pygame.mouse.set_visible(False)

    def jetHit(self):
        """Respond to the jet being hit by an plane."""
        if self.stats.jetsLeft > 0:
            # Decrement jets_left.
            self.stats.jetsLeft -= 1
            self.sb.prepJets() 

            # Get rid of any remaining planes and bullets.
            self.planes.empty()
            self.bullets.empty()

            # Create a new fleet and center the jet.
            self.createFleet() 
            self.jet.centerJet()

            # Pause.
            sleep(0.5)
        else:
            self.stats.gameActive = False
            pygame.mouse.set_visible(True)
        

    def createFleet(self):
        """Create the fleet of planes."""
        # Create an plane and find the number of planes in a row.
        # Spacing between each plane is equal to one plane width.
        plane = Plane(self)
        planeWidth, planeHeight = plane.rect.size
        availableSpaceX = self.settings.screenWidth - (2 * planeWidth)
        numberPlanesX = availableSpaceX // (2 * planeWidth)

        # Determine the number of plane rows
        jetHeight = self.jet.rect.height
        availableSpaceY = (self.settings.screenHeight - (3 * planeHeight) - jetHeight)
        numberRows = availableSpaceY // (2 * planeHeight)

        # Create full fleet of planes.
        for rowNumber in range(numberRows):
            for planeNumber in range(numberPlanesX):
                self.createPlane(planeNumber, rowNumber)

    def createPlane(self, planeNumber, rowNumber):
        plane = Plane(self)
        planeWidth, planeHeight = plane.rect.size
        plane.x = planeWidth + 2 * planeWidth * planeNumber
        plane.rect.x = plane.x
        plane.rect.y = plane.rect.height + 2 * plane.rect.height * rowNumber
        self.planes.add(plane)

    def updatePlanes(self):
        """ Update positon of all planes """
        self.checkFleetEdges()
        self.planes.update()

        # look for plane and jet collision
        if pygame.sprite.spritecollideany(self.jet, self.planes):
            self.jetHit()

        # look for planes hitting bottom
        self.checkPlanesBottom()

    def checkFleetEdges(self):
        """Respond appropriately if any planes have reached an edge."""
        for plane in self.planes.sprites():
            if plane.checkEdges():
                self.changeFleetDirection()
                break

    def changeFleetDirection(self):
        """Drop the entire fleet and change the fleet's direction."""
        for plane in self.planes.sprites():
            plane.rect.y += self.settings.fleetDropSpeed
        self.settings.fleetDirection *= -1

    def checkPlanesBottom(self):
        """Check if any planes have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for plane in self.planes.sprites():
            if plane.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the jet got hit.
                self.jetHit()
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

        self.checkBulletPlaneCollisions()

    def checkBulletPlaneCollisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.planes, True, True)

        if collisions:
            for planes in collisions.values():
                self.stats.score += self.settings.planePoints * len(planes)
            self.sb.prepScore()
            self.sb.checkHighScore()
            pygame.mixer.music.play(1)

        if not self.planes:
            #destroy exisiting bullets and create new fleet
            self.bullets.empty()
            self.createFleet()
            self.settings.increaseSpeed()

            # Increase level
            self.stats.level += 1
            self.sb.prepLevel()

    def updateScreen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.settings.bg, (0,0))
        self.jet.blitme()

        for bullet in self.bullets.sprites():
            bullet.drawBullet()
        self.planes.draw(self.screen)

        #draw score info
        self.sb.showScore()

        # draw the play button if the game is inactive.
        if not self.stats.gameActive:
            self.playButton.drawButton()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = JetFighter()
    ai.runGame()