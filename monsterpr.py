"""
Ali Salem, 
Monsters Inc (Group 7)
Prof. Iskander
INST 326

A program that acts as like game disguised as a screen saver

Within the screen saver, there will be a calander, a time, a character
that either follows the mouse cursor, or controlled by the arrow keys
"""
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720)) # placeholder screen size
pygame.display.set_caption("Monsters Inc Screen Saver")


class Character:
    pass

class DateDisplay:
    pass

class TimeDisplay:
    pass

class QuoteDisplay:
    pass

class Background:
    pass


def main():
    """Runs the Pygame window

    """
    clock = pygame.time.Clock()
    running = True

    # Background color: black
    bg_color = (0, 0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen with background color
        screen.fill(bg_color)

        # Flip the display buffers
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
