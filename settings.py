class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screenWidth = 1200
        self.screenHeight = 800
        self.bgColor = (230, 230, 230)

        # Ship settings
        self.shipSpeed = 1.5
        self.shipLimit = 3

        # Bullet settings
        self.bulletSpeed = 1.5
        self.bulletWidth = 3
        self.bulletHeight = 15
        self.bulletColor = (60, 60, 60)
        self.bulletsAllowed = 3

        #alien settings
        self.alienSpeed = 1.0
        self.fleetDropSpeed = 10
        self.fleetDirection = 1

        # how quickly the game speeds up
        self.speedUpScale = 1.1

        # how quickly the alien points increase
        self.scorScale = 1.5

        self.initializeDynamicSettings()

    def initializeDynamicSettings(self):
        """Initialize settings that change throughout the game."""
        self.shipSpeed = 1.5
        self.bulletSpeed = 3.0
        self.alienSpeed = 1.0

        #scoreing
        self.alienPoints = 50

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleetDirection = 1

    def increaseSpeed(self):
        """Increase speed settings and alien point values"""
        self.shipSpeed *= self.speedUpScale
        self.bulletSpeed *= self.speedUpScale
        self.alienSpeed *= self.speedUpScale
        self.alienPoints = int(self.alienPoints * self.scorScale)