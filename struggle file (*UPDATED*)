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
    pass

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

def main():
    """
    Runs the Pygame window
    """
    clock = pygame.time.Clock()
    running = True

    bg_gradient = Background(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen with background color
     

        # Flip the display buffers
        pygame.display.flip()

        # Cap the frame rate
        bg_gradient.draw()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
