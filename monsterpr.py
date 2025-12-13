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
    args:
        starting_pos (tuple): The starting (x, y) position of the character.
        coordinates (tuple): The current (x, y) position of the character.
        speed (int): The movement speed of the character.
        x (int): The current x-coordinate of the character.
        y (int): The current y-coordinate of the character.
        
    returns:
        None
    raises:
        None
    """
    starting_pos = (640, 360)  # Start in the center of the screen
    def __init__(self, starting_pos=starting_pos):
        """Initializes the character at the starting position."""
        
        coordinates = starting_pos
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.speed = 3  # Movement speed
    def drawcharacter(self, screen):
        """Draws the character at its current position."""
        # Placeholder for character drawing logic
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 20)  # Draw a red circle as the character
        
    def move_up(self):
        """Moves the character up."""
        self.y -= self.speed
        
    def move_down(self):
        """Moves the character down."""
        self.y += self.speed
        
    def move_left(self):
        """Moves the character left."""
        self.x -= self.speed
        
    def move_right(self):
        """Moves the character right."""
        self.x += self.speed
    
    
    
        

class DateDisplay:
    """
    Displays the current date on the screen with the format of 00/00/0000
    
    Args:
        screen (pygame.Surface): The Pygame surface where the date will be displayed.
        x (int): The x-coordinate
        y (int): The y-coordinate
        today (str): The current date in MM/DD/YYYY format.
        text_surface (pygame.Surface): The surface containing the rendered date text.
        text_h (int): The height of the rendered text.
        
    Returns:
        None
    Raises:
        None
    """
    def __init__(self, screen, x=20, y=None):
        """
        initializes the DateDisplay class with the screen, x and y coordinates, font, and color.
        """
        self.screen = screen
        self.font = pygame.font.SysFont('Consolas', 28)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self):
        """
        draws the current date onto the screen as a surface, then blit(applies) the surface onto the window.
        """
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        text_surface = self.font.render(today, True, self.color) #renders text onto the surface
        _, text_h = self.font.size(today) # the underscore is used to ignore the text_w (width) because we dont need it
        # place bottom-left if y not specified
        if self.y is None:
            self.y = self.screen.get_height() - text_h - 10
        self.screen.blit(text_surface, (self.x, self.y)) #puts the surface onto the screen


class TimeDisplay:
    """
    Display the current time in the system 00:00 AM/PM format.
    Args:
        screen (pygame.Surface): The Pygame surface where the time will be displayed.
        x (int): The x-coordinate
        y (int): The y-coordinate
        color (tuple): RGB color for the text, currently set to white.
        
    returns:
        None
    raises:
        None
    """
    def __init__(self, screen, x=None, y=None):
        """
        initializes the TimeDisplay class with the screen, x and y coordinates, font, and color.
        """
        self.screen = screen
        self.font = pygame.font.SysFont('Consolas', 28)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)

    def draw(self):
        """
        draws the current time onto the screen as a surface, then blit(applies) the surface onto the window.
        """
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        text_surface = self.font.render(current_time, True, self.color) #renders text onto the surface
        text_w, text_h = self.font.size(current_time)
        # center horizontally if x not specified
        if self.x is None:
            self.x = (self.screen.get_width() - text_w) // 2
        # place at bottom if y not specified
        if self.y is None:
            self.y = self.screen.get_height() - text_h - 10
        self.screen.blit(text_surface, (self.x, self.y)) #puts surface onto the screen
        

class QuoteDisplay:
    """
    Displays the motivational quote on the screen and changes every 5th minute on the system clock.
    Args:
        screen (pygame.Surface): The Pygame surface where the quote will be displayed.
        timeblock (int): The current time block for quote updates. example 0-4 minutes is block 0, 5-9 is block 1, etc.
        current_quote (str): The currently displayed quote.
        current_author (str): The author of the currently displayed quote.
        dfquotes (pd.DataFrame): DataFrame containing quotes and authors loaded from CSV.
        dfquotesfiltered (pd.DataFrame): Filtered DataFrame with non-empty authors.
        dfquotesfilterfinal (pd.DataFrame): Further filtered DataFrame with quotes shorter than 95 characters.
    Returns:
        None
    Raises:
        None
    """
    #load quotes from csv into dataframe
    dfquotes = pd.read_csv("quotes.csv")

    #remove empty author rows
    dfquotesfiltered = dfquotes.dropna(subset=["Author"])
    #filter quotes longer than 95 characters
    dfquotesfilterfinal = dfquotesfiltered[dfquotesfiltered["Quote"].str.len() < 95] 
    
    def __init__(self, screen):
        """
        initializes the QuoteDisplay class with the screen, font, timeblock, current_quote, and current_author.
        """
        self.screen = screen 
        self.font = pygame.font.SysFont('Consolas', 24)
        self.timeblock = -1 #acts like a block, it is negative to ensure that a random quote displays immediately
        self.current_quote = "" #initialize with empty quote
        self.current_author = "" #initialize with empty author
        self.update_quote()  # Set initial quote

    def update_quote(self):
        """
        Updates the quote if the current time block has changed.
        """
        current_minute = datetime.datetime.now().minute  #grabs the current system minute, and only the minute
        if current_minute // 5 != self.timeblock:# Update every 5 minutes
            self.timeblock = current_minute // 5  
            random_quote = self.dfquotesfilterfinal.sample().iloc[0] #selects a random cell
            self.current_quote = random_quote["Quote"] #gets the quote from the cell
            self.current_author = random_quote["Author"] #get the author from the cell

    def draw(self):
        """
        Draws the quote and author onto the screen.
        """
        quote_text = self.font.render(f'"{self.current_quote}"', True, (255, 255, 255)) #writes the quote text to the surface
        author_text = self.font.render(f'- {self.current_author}', True, (255, 255, 255)) #writes the author text to the surface
        self.screen.blit(quote_text, (20, 20)) #displays the surface on the screen
        self.screen.blit(author_text, (20, 50)) #displays the surface on the screen


    
    
class Background:
    """
    Manages the background images and smoothly fades between.
    This works by drawing the current image, and then adding another image on top
    with an increasing alpha(transparency) untill it is no longer transparent
    Args:
        screen (pygame.Surface): The Pygame surface where the background will be displayed.
        images (list): List of loaded background images.
        current (int): Index of the current background image.
        next (int): Index of the next background image to fade into.
        fade_duration (int): Duration of the fade effect in milliseconds.
        last_switch (int): Timestamp of the last image switch.
        fade_start (int): Timestamp when the fade started.
        is_fading (bool): Flag indicating if a fade is currently in progress.
        
    Returns:
        None
    Raises:
        ValueError: If an unsupported file format is encountered in the background images folder.
        
    """
    def __init__(self, screen):
        """
        initializes the Background class with the screen, loads images from the specified folder
        """
        self.screen = screen
        folder = "Background images for 326 pr"

        
        self.images = [] #empty list
        for file in os.listdir(folder): #load all images in the folder
            if file.endswith('.png') or file.endswith('.jpg'): #check for valid image file types, just incase we decide to add more backgrounds that have different file types
                img = pygame.image.load(os.path.join(folder, file)).convert_alpha() #important for the images to have transparency to be able to fade
                self.images.append(img) #add image to list
            else:
                raise ValueError("ERROR: Unsupported file format! Only .png and .jpg are supported.")
        # Image indexes
        self.current = 0
        self.next = 1

        # Fade timing
        self.fade_duration = 15000      #  15 seconds fade
        self.last_switch = pygame.time.get_ticks()
        self.fade_start = None
        self.is_fading = False

    def draw(self):
        """Draw the current image."""
        self.screen.blit(self.images[self.current], (0, 0)) #draws the image

    def start_fade(self):
        """
        Start the fade into the next image. 
        keeps track of the time the fade started.
        """
        self.fade_start = pygame.time.get_ticks()
        self.is_fading = True
        self.next = (self.current + 1) % len(self.images)

    def updatescreen(self):
        """
        Updates background and handles fade transitions.
        """
        now = pygame.time.get_ticks()

        # Trigger fade every 2 seconds
        if now - self.last_switch >= 2000 and not self.is_fading:
            self.last_switch = now
            self.start_fade()

        if self.is_fading:
            elapsed = now - self.fade_start
            alpha = min(255, int((elapsed / self.fade_duration) * 255))

            # the current image
            self.screen.blit(self.images[self.current], (0, 0))

            # the next image fading in
            fade_img = self.images[self.next].copy()
            fade_img.set_alpha(alpha) #set transparency level
            self.screen.blit(fade_img, (0, 0)) #draws the image on top of the base layer as it fades

            # fade complete
            if elapsed >= self.fade_duration:
                self.current = self.next
                self.is_fading = False

        else:
            self.draw()


def main():
    """
    Runs the Pygame window
    1. Initializes Pygame and sets up the display.
    2. Creates instances of Background, QuoteDisplay, DateDisplay, TimeDisplay, and Character.
    3. Enters the main loop to handle events, update game state, and render the screen.
    4. Exits cleanly when the user quits with 'Esc'.
    5. contains movement controls for the character using arrow keys.
    6. Contains fullscreen toggle using 'f' key.
    Returns:
        None
    Raises:
        None
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
        

        # takes everything we drew and puts it on the screen surface
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
