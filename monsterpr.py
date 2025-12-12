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
import pandas as pd

pygame.init()

screen = pygame.display.set_mode((1280, 720)) # placeholder screen size
pygame.display.set_caption("Monsters Inc Screen Saver") #window caption


class Character:
    """
    A moveable character that follows the mouse cursor or is controlled by arrow keys.
    """
    starting_pos = (640, 360)  # Start in the center of the screen
    def __init__(self):
        
        coordinates = Character.starting_pos
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.speed = 5  # Movement speed
    def drawcharacter(self, screen):
        # Placeholder for character drawing logic
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 20)  # Draw a red circle as the character
        
    def move_up(self):
        self.y -= self.speed
        
    def move_down(self):
        self.y += self.speed
        
    def move_left(self):
        self.x -= self.speed
        
    def move_right(self):
        self.x += self.speed
    
    
        

class DateDisplay:
    """
    Displays the current date on the screen with the format of 00/00/0000
    """
    def __init__(self, screen, x=20, y=None):
        self.screen = screen
        self.font = pygame.font.SysFont('Consolas', 28)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self):
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        text_surface = self.font.render(today, True, self.color)
        _, text_h = self.font.size(today) # the underscore is used to ignore the text_w (width) because we dont need it
        # place bottom-left if y not specified
        if self.y is None:
            self.y = self.screen.get_height() - text_h - 10
        self.screen.blit(text_surface, (self.x, self.y))


class TimeDisplay:
    """
    Display the current time in the system 00:00 AM/PM format.
    """
    def __init__(self, screen, x=None, y=None):
        self.screen = screen
        self.font = pygame.font.SysFont('Consolas', 28)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        text_surface = self.font.render(current_time, True, self.color)
        text_w, text_h = self.font.size(current_time)
        # center horizontally if x not specified
        if self.x is None:
            self.x = (self.screen.get_width() - text_w) // 2
        # place at bottom if y not specified
        if self.y is None:
            self.y = self.screen.get_height() - text_h - 10
        self.screen.blit(text_surface, (self.x, self.y))
        

class QuoteDisplay:
    """
    Displays the motivational quote on the screen and changes every 5th minute on the clock.
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
        self.timeblock = -1 #acts like a block, it is negative to ensure that a random quote displays immediately
        self.current_quote = "" #initialize with empty quote
        self.current_author = "" #initialize with empty author
        self.update_quote()  # Set initial quote

    def update_quote(self):
        current_minute = datetime.datetime.now().minute  #grabs the current system minute, and only the minute
        if current_minute // 5 != self.timeblock:# Update every 5 minutes
            self.timeblock = current_minute // 5  
            random_quote = self.dfquotesfilterfinal.sample().iloc[0] #selects a random cell
            self.current_quote = random_quote["Quote"] #gets the quote from the cell
            self.current_author = random_quote["Author"] #get the author from the cell

    def draw(self):
        quote_text = self.font.render(f'"{self.current_quote}"', True, (255, 255, 255))
        author_text = self.font.render(f'- {self.current_author}', True, (255, 255, 255))
        self.screen.blit(quote_text, (20, 20))
        self.screen.blit(author_text, (20, 50))


    
    
class Background:
    """
    Manages the background images and smoothly fades between.
    This works by drawing the current image, and then adding another image on top
    with an increasing alpha(transparency) untill it is no longer transparent
    """
    def __init__(self, screen):
        self.screen = screen
        folder = "Background images for 326 pr"

        
        self.images = [] #empty list
        for file in os.listdir(folder): #load all images in the folder
            if file.endswith('.png') or file.endswith('.jpg'): #check for valid image file types, just incase we decide to add more backgrounds that have different file types
                img = pygame.image.load(os.path.join(folder, file)).convert_alpha() #important for the images to have transparency to be able to fade
                self.images.append(img) #add image to list

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
        self.screen.blit(self.images[self.current], (0, 0)) #acts as a placeholder

    def start_fade(self):
        """
        Start the fade into the next image. 
        keeps track of the time the fade started.
        """
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
    
    quote_display = QuoteDisplay(screen)
    
    date_display = DateDisplay(screen)
    time_display = TimeDisplay(screen)
    
    player = Character()


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
            
        #movement
        key = pygame.key.get_pressed() # detects if key is held down
        if key[pygame.K_UP]:
            player.move_up()
        elif key[pygame.K_DOWN]:
            player.move_down()
        elif key[pygame.K_LEFT]:
            player.move_left()
        elif key[pygame.K_RIGHT]:
            player.move_right()
     

        # Update background, draw UI elements, then flip the display buffers
        
        bg_gradient.updatescreen()
        player.drawcharacter(screen)
        
        quote_display.update_quote()
        quote_display.draw()
        
        date_display.draw()
        time_display.draw()
        

        # Flip the display buffers
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
