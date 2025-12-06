"""
Ali Salem, Solii.M
Monsters Inc (Group 7)
Prof. Iskander
INST 326

A program that acts as like game disguised as a screen saver

Within the screen saver, there will be a calander, a time, a character
that either follows the mouse cursor, or controlled by the arrow keys

Background iterates through different backgrounds every 4 hours
"""
import pygame
import os 
import datetime
import random
import pandas as pd

pygame.init()

screen = pygame.display.set_mode((1280, 720)) # placeholder screen size
pygame.display.set_caption("Monsters Inc Screen Saver")


class Character:
    """
    A moveable character that follows the mouse cursor or is controlled by arrow keys.
    """
    pass

class DateDisplay:
    """
    Displays the current date on the screen with the format of 00/00/0000
    """
    pass

class TimeDisplay:
    """
    display the current time in the system 00:00 AM/PM format.
    """
    pass

class QuoteOfTheDayDisplay:
    """
    Displays the motivational quote on the screen and changes with the background every 4 hours.
    """
    #load quotes from csv into dataframe
    dfquotes = pd.read_csv("quotes.csv")

    #remove empty author rows
    dfquotesfiltered = dfquotes.dropna(subset=["Author"])

    def __init__(self, screen):
        self.screen = screen 
        self.font = pygame.font.SysFont('Consolas', 24)
        self.last_change_hour = -1
        self.current_quote = "" #initialize with empty quote
        self.current_author = "" #initialize with empty author
        self.update_quote()  # Set initial quote

    def update_quote(self):
        current_hour = datetime.datetime.now().hour
        if current_hour // 4 != self.last_change_hour:
            self.last_change_hour = current_hour // 4
            random_quote = self.dfquotesfiltered.sample().iloc[0]
            self.current_quote = random_quote["Quote"]
            self.current_author = random_quote["Author"]

    def draw(self):
        quote_text = self.font.render(f'"{self.current_quote}"', True, (255, 255, 255))
        author_text = self.font.render(f'- {self.current_author}', True, (255, 255, 255))
        self.screen.blit(quote_text, (20, 20))
        self.screen.blit(author_text, (20, 50))

    
    
class Background:
    """
    Manages the background images and changes them every 4 hours.
    """
    def __init__(self, screen): 
        self.screen = screen
        folder = "Background images for 326 pr"
    
        self.images = []
        for file in os.listdir(folder):
            if file.endswith('.png') or file.endswith('.jpg'):
                self.images.append(
                    pygame.image.load(os.path.join(folder,file)).convert()
            )
        self.current = 0
    def draw(self):
        self.screen.blit(self.images[self.current], (0, 0))

    def updatescreen(self):
        now = pygame.time.get_ticks()

        # If 2 seconds passed, move to the next image
        if now - self.last_change >= self.change_interval:
            self.current = (self.current + 1) % len(self.images)
            self.last_change = now

        self.draw()


def main():
    """
    Runs the Pygame window
    """
    clock = pygame.time.Clock()
    running = True

    bg_gradient = Background(screen)
    bg_gradient.last_change = pygame.time.get_ticks()
    bg_gradient.change_interval = 4 * 60 * 60 * 1000  # 4 hours in milliseconds

    quote_display = QuoteOfTheDayDisplay(screen)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

     

        # Flip the display buffers
        pygame.display.flip()
        bg_gradient.updatescreen()
        
        quote_display.update_quote()
        quote_display.draw()
    
        # Cap the frame rate
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
