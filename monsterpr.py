"""
Ali Salem, Solii.M, Ibrahim Ahmed, 
Monsters Inc (Group 7)
Prof. Iskander
INST 326

A program that acts as like game disguised as a screen saver

Within the screen saver, there will be a calander, a time, a character 
controlled by the arrow keys

Background fades smoothly between images, quote updates every hour or every time yqou open the program
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
    def __init__(self, screen, x=1100, y=20):
        self.screen = screen
        self.font = pygame.font.SysFont('Consolas', 28)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self):
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        text_surface = self.font.render(today, True, self.color)
        self.screen.blit(text_surface, (self.x, self.y))


class TimeDisplay:
      """
    display the current time in the system 00:00 AM/PM format.
    """
    def __init__(self, screen, x=1100, y=60):
        self.screen = screen 
        self.font = pygame.font.SysFont('Consolas', 28)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        text_surface = self.font.render(current_time, True, self.color)
        self.screen.blit(text_surface, (self.x, self.y))
        

class QuoteOfTheDayDisplay:
    """
    Displays the motivational quote on the screen and changes with the background every 4 hours.
    """
    #load quotes from csv into dataframe
    dfquotes = pd.read_csv("quotes.csv")

    #remove empty author rows
    dfquotesfiltered = dfquotes.dropna(subset=["Author"])
    #filter quotes longer than 95 characters
    dfquotesfilterfinal = dfquotesfiltered[dfquotesfiltered["Quote"].str.len() < 95] 
    
    def __init__(self, screen):
        self.screen = screen 
        self.font = pygame.font.SysFont('Consolas', 24)
        self.last_change_hour = -1
        self.current_quote = "" #initialize with empty quote
        self.current_author = "" #initialize with empty author
        self.update_quote()  # Set initial quote

    def update_quote(self):
        current_hour = datetime.datetime.now().hour
        if current_hour // 1 != self.last_change_hour:
            self.last_change_hour = current_hour // 1  # Update every hour
            random_quote = self.dfquotesfilterfinal.sample().iloc[0]
            self.current_quote = random_quote["Quote"]
            self.current_author = random_quote["Author"]

    def draw(self):
        quote_text = self.font.render(f'"{self.current_quote}"', True, (255, 255, 255))
        author_text = self.font.render(f'- {self.current_author}', True, (255, 255, 255))
        self.screen.blit(quote_text, (20, 20))
        self.screen.blit(author_text, (20, 50))


    
    
class Background:
    """
    Manages the background images and smoothly fades between.
    """
    def __init__(self, screen):
        self.screen = screen
        folder = "Background images for 326 pr"

        # Load images
        self.images = []
        for file in os.listdir(folder):
            if file.endswith('.png') or file.endswith('.jpg'):
                img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
                self.images.append(img)

        # Image indices
        self.current = 0
        self.next = 1

        # Fade timing
        self.fade_duration = 15000      #  15 seconds fade
        self.last_switch = pygame.time.get_ticks()
        self.fade_start = None
        self.is_fading = False

    def draw(self):
        """Draw the current image when not fading."""
        self.screen.blit(self.images[self.current], (0, 0))

    def start_fade(self):
        """Start the fade into the next image."""
        self.fade_start = pygame.time.get_ticks()
        self.is_fading = True
        self.next = (self.current + 1) % len(self.images)

    def updatescreen(self):
        """Updates background and handles fade transitions."""
        now = pygame.time.get_ticks()

        # Trigger fade every 2 seconds
        if now - self.last_switch >= 2000 and not self.is_fading:
            self.last_switch = now
            self.start_fade()

        if self.is_fading:
            elapsed = now - self.fade_start
            alpha = min(255, int((elapsed / self.fade_duration) * 255))

            # base layer (current)
            self.screen.blit(self.images[self.current], (0, 0))

            # fading layer (next)
            fade_img = self.images[self.next].copy()
            fade_img.set_alpha(alpha)
            self.screen.blit(fade_img, (0, 0))

            # fade complete
            if elapsed >= self.fade_duration:
                self.current = self.next
                self.is_fading = False

        else:
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
    
    date_display = DateDisplay(screen)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            #fullscreen toggle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f: # Press 'f' to toggle fullscreen
                    pygame.display.toggle_fullscreen()
            

       
     

        # Flip the display buffers
        pygame.display.flip()
        bg_gradient.updatescreen()
        
        quote_display.update_quote()
        quote_display.draw()
        
        date_display.draw()

    
        # Cap the frame rate
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
