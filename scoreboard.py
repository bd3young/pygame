import pygame.font
class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.screen = ai_game.screen
        self.screenRect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.textColor = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prepScore()

    def prepScore(self):
        """Turn the score into a rendered image."""
        scoreStr = str(self.stats.score)
        self.scoreImage = self.font.render(scoreStr, True, self.textColor, self.settings.bgColor)

        # Display the score at the top right of the screen.
        self.scoreRect = self.scoreImage.get_rect()
        self.scoreRect.right = self.screenRect.right - 20
        self.scoreRect.top = 20
    
    def showScore(self):
        """ draw score on screen """
        self.screen.blit(self.scoreImage, self.scoreRect)