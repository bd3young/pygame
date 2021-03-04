class GameStats:
    """Track statistics for Alien Invasion."""
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.resetStats()
        self.gameActive = False

    def resetStats(self):
        """Initialize statistics that can change during the game."""
        self.shipsLeft = self.settings.shipLimit
        self.score = 0