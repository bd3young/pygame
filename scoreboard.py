import pygame.font
from pygame.sprite import Group
from jet import Jet

class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.aiGame = ai_game
        self.screen = ai_game.screen
        self.screenRect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.textColor = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prepScore()
        self.prepHighScore()
        self.prepLevel()
        self.prepJets()

    def prepScore(self):
        """Turn the score into a rendered image."""
        roundedScore = round(self.stats.score, - 1)
        scoreStr = "{:,}".format(roundedScore)
        self.scoreImage = self.font.render(scoreStr, True, self.textColor, self.settings.bgColor)

        # Display the score at the top right of the screen.
        self.scoreRect = self.scoreImage.get_rect()
        self.scoreRect.right = self.screenRect.right - 20
        self.scoreRect.top = 20

    def prepHighScore(self):
        """Turn the high score into a rendered image."""
        highScore = round(self.stats.highScore, -1)
        highScoreStr = "{:,}".format(highScore)
        self.highScoreImage = self.font.render(highScoreStr, True, self.textColor, self.settings.bgColor)

        # Center the high score at the top of the screen.
        self.highScoreRect = self.highScoreImage.get_rect()
        self.highScoreRect.centerx = self.screenRect.centerx
        self.highScoreRect.top = self.scoreRect.top

    def prepLevel(self):
        """Turn the level into a rendered image."""
        levelStr = str(self.stats.level)
        self.levelImage = self.font.render(levelStr, True,
        self.textColor, self.settings.bgColor)

        # Position the level below the score.
        self.levelRect = self.levelImage.get_rect()
        self.levelRect.right = self.scoreRect.right
        self.levelRect.top = self.scoreRect.bottom + 10

    def prepJets(self):
        """Show how many jets are left."""
        self.jets = Group()
        for shipNumber in range(self.stats.shipsLeft):
            jet = Jet(self.aiGame)
            jet.rect.x = 10 + shipNumber * jet.rect.width
            jet.rect.y = 10
            self.jets.add(jet)

    def checkHighScore(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.highScore:
            self.stats.highScore = self.stats.score
            self.prepHighScore()    
    
    def showScore(self):
        """ draw score and level on screen """
        self.screen.blit(self.scoreImage, self.scoreRect)
        self.screen.blit(self.highScoreImage, self.highScoreRect)
        self.screen.blit(self.levelImage, self.levelRect)
        self.jets.draw(self.screen)

    