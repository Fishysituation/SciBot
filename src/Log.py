"""This file defines the command log class."""
import pygame

class Log:
    """This class defines the command log."""

    def __init__(self,
                 text_colour, # The colour of the text
                 background_colour, # The colour of the background
                 screen_location, # The position on the screen
                 size): # size of rect to be drawn (width, height)
        """Create a command log"""
        self.text_colour = text_colour
        self.background_colour = background_colour
        self.screen_location = screen_location
        self.size = size
        self.rect = pygame.Rect(screen_location, size)
        self.font = pygame.font.SysFont("comicsansms", 28)
        self.title_width = 150

        self.entry_location = (
            screen_location[0] + self.title_width,
            screen_location[1]
        )
        # calculate number of entries that can be held as the floor
        # of width of entry area / smallest acceptable entry width
        self.max_entry_no = int((self.size[0]-self.title_width)/110)
        # calculate the size of each entry
        self.entry_width = int((self.size[0]-self.title_width)/self.max_entry_no)

        self.commands = [] # List of all entry instances
        self.current = [] # splice of self.commands to be displayed

        self.Pointer = Pointer((255, 0, 0), self)
    
    def clear_log(self):
        """Clear command log and queue"""
        self.commands = []
        self.current = []


    def display(self, screen):
        """Display the log box"""
        #Draw a black border
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect,
            4
        )

        text = self.font.render(
            "CMD LOG",
            True,
            self.text_colour,
        )

        #Draws one line at x = self.entry_location
        for i in range(0, 1):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (self.entry_location[0] + i * self.entry_width, self.screen_location[1]),
                (self.entry_location[0] + i * self.entry_width, self.screen_location[1]+90),
                4
            )

        text_rect = text.get_rect()
        text_rect.centerx = self.title_width/2
        text_rect.centery = self.screen_location[1] + (self.size[1]/2)
        screen.blit(text, text_rect)

        
        for i in range(0, len(self.current)):
            self.current[i].display(screen)
        

    def draw_entry(self, screen):
        """Display all instances in self.current"""
        iterations = self.max_entry_no
        if iterations > len(self.current):
            iterations = len(self.current)

        for i in  range(0, iterations):
            self.current[i].display(screen)

    def add_entry(self, text):
        """Add entry to self.commands / self.current"""
        #cap queue_no at self.max_entry_no
        queue_no = len(self.commands)
        if queue_no >= self.max_entry_no:
            queue_no = self.max_entry_no -1
            # remove first entry in list
            self.current = self.current[1:]
            for i in range(0, self.max_entry_no-1):
                # Move each entry one step left
                self.current[i].move(self.entry_width)

        new_entry = Entry(
            text,
            (0, 0, 0),
            (255, 255, 255),
            len(self.commands),
            queue_no,
            self
        )
        self.commands.append(new_entry)
        self.current.append(new_entry)


class Entry:
    """This class defines a log entry"""

    def __init__(self,
                 text, # Text to display
                 text_colour, # Colour of text
                 background_colour, # Colour of background
                 queue_no, # Position of instruction in Beebot.memory
                 log_no, # Position of instruction to display in log
                 cmd): # Log object
        """Create a log entry"""
        self.text = str(queue_no+1) + ". " + text
        self.text_colour = text_colour
        self.background_colour = background_colour
        self.queue_no = queue_no # index of instruction
        self.log_no = log_no # position in log to display entry
        self.font = pygame.font.SysFont("comicsansms", 24)


        startx = cmd.entry_location[0]
        starty = cmd.entry_location[1]
        width = cmd.entry_width
        self.coords = (
            startx + (width * log_no) + 7,
            starty + 7
        )
        self.rect = pygame.Rect(
            (startx + (width * log_no) + 7,
             starty + 7),
            (width-10, 50)
        )

    def display(self, screen):
        """Draw the Entry object on the screen"""
        screen.fill(self.background_colour, rect=self.rect)

        # Draw the Entry text
        text = self.font.render(self.text,
                                True,
                                self.text_colour)

        # Center the background and text
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.centerx
        text_rect.centery = self.rect.centery

        # Render Entry on screen
        screen.blit(text, text_rect)

    def move(self, x):
        """Move entry instance one logical step left"""
        self.rect = self.rect.move(-x, 0)

    def swap_colours(self):
        """Swap text and background colours of the entry"""
        temp_colour = self.text_colour
        self.text_colour = self.background_colour
        self.background_colour = temp_colour
        self.swapped = not self.swapped


class Pointer:
    """This class defines the current instruction pointer"""
    def __init__(self, colour, cmd):
        """Create a pointer"""
        self.colour = colour
        
        self.pos = 0 # queue no. to point at
        
        startx = cmd.entry_location[0]
        starty = cmd.entry_location[1]
        length = cmd.entry_width
        height = cmd.size[1]
        self.shape = (
            (startx + int(length/2) - 20, starty + height - 4),
            (startx + int(length/2) + 20, starty + height - 4),
            (startx + int(length/2), starty + height - 20 - 4),
        )

    def display(self, screen):
        """Draw pointer triangle"""
        pygame.draw.polygon(screen, self.colour, self.shape)

    def move():
        """Move the pointer to next item in queue"""
        print("TODO")