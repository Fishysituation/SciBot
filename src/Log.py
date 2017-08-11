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


    def display(self, screen, running):
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

        # Draws one line at x = self.entry_location:
        # Change range (0, self.max_entry_no) to draw
        # line after each entry
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

        # display all entries in self.current
        for i in range(0, len(self.current)):
            self.current[i].display(screen)

        if running:
            self.Pointer.display(screen)


    def set_pos(self):
        """Changes position of all entries in self.current to display position"""
        for i in range(0, len(self.current)):
            # ignore entries that need not be moved
            if self.current[i].log_no != i:
                # move Entry into place
                self.current[i].move(
                    i-self.current[i].log_no,
                    self.entry_width
                )
                # set log_no
                self.current[i].log_no = i


    def add_entry(self, text):
        """Add entry to self.commands and self.current"""
        queue_no = len(self.commands)
        if queue_no >= self.max_entry_no:
        #cap queue_no at self.max_entry_no
            queue_no = self.max_entry_no -1
            # remove first element from self.current
            self.current = self.current[1:]

        new_entry = Entry(
            text,
            (0, 0, 0),
            (255, 255, 255),
            len(self.commands),
            0,
            self
        )
        self.commands.append(new_entry)
        # add to current by reference
        self.current.append(new_entry)
        # move all entries into correct position
        self.set_pos()



    def push_entry(self, index):
        """Push next entry to command log when running"""
        # revert colour of previous Entry
        self.unswap()
        # if the entries do not need to be moved 
        if index < self.max_entry_no:
            # move the pointer to the next Entry
            self.Pointer.move(self.entry_width)
            # swap the colour of the Entry
            self.current[index].swap_colours()
        else:
            # remove first in queue
            self.current = self.current[1:]
            # add the next in queue to Log
            self.current.append(self.commands[index])
            # move all entries into place
            self.set_pos()
            # swap colours of next entry
            self.current[-1].swap_colours()


    def unswap(self):
        """Unswaps colours of Entry"""
        for i in range(0, len(self.commands)):
            if self.commands[i].swapped == True:
                self.commands[i].swap_colours()

    def reset_pointer(self):
        """Reset the position of the pointer"""
        self.Pointer.shape = self.Pointer.original


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
        self.swapped = False


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


    def move(self, x, step_width):
        """Move entry instance x logical steps left"""
        self.rect = self.rect.move(x * step_width, 0)


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
        self.original = (
            (startx + int(length/2) - 20, starty + height - 4),
            (startx + int(length/2) + 20, starty + height - 4),
            (startx + int(length/2), starty + height - 20 - 4),
        )
        self.shape = self.original

    def display(self, screen):
        """Draw pointer triangle"""
        pygame.draw.polygon(screen, self.colour, self.shape)

    def move(self, x):
        """Move the pointer to next item in queue"""
        self.copyof = []
        for i in range(0, 3):
            self.copyof.append(
                (self.shape[i][0] + x,
                 self.shape[i][1])
            )
        self.shape = self.copyof
