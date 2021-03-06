import pygame

class Settings:
    """A class to store all settings for Jet Fighter."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screenWidth = 1200
        self.screenHeight = 800
        self.bgColor = (230, 230, 230)
        self.bg = pygame.image.load("images\skyBackground.jpg")

        # Ship settings
        self.jetSpeed = 1.5
        self.jetLimit = 3

        # Bullet settings
        self.bulletSpeed = 1.5
        self.bulletWidth = 7
        self.bulletHeight = 15
        self.bulletColor = (60, 60, 60)
        self.bulletsAllowed = 4
        self.explosion = pygame.mixer.music.load("audio\explosion.wav")

        #plane settings
        self.planeSpeed = 2.0
        self.fleetDropSpeed = 20
        self.fleetDirection = 1

        # how quickly the game speeds up
        self.speedUpScale = 1.1

        # how quickly the plane points increase
        self.scorScale = 1.5

        self.initializeDynamicSettings()

    def initializeDynamicSettings(self):
        """Initialize settings that change throughout the game."""
        self.jetSpeed = 1.5
        self.bulletSpeed = 3.0
        self.planeSpeed = 1.0

        #scoreing
        self.planePoints = 50

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleetDirection = 1

    def increaseSpeed(self):
        """Increase speed settings and plane point values"""
        self.jetSpeed *= self.speedUpScale
        self.bulletSpeed *= self.speedUpScale
        self.planeSpeed *= self.speedUpScale
        self.planePoints = int(self.planePoints * self.scorScale)