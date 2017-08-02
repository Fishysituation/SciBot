"""This file defines the Button class."""
import pygame
from enum import Enum

class Arrow(Enum):
    """This class defines Enums for the arrow polygon of a button"""
    #array of vectors for each arrow
    UP = [
        (20, -20),
        (0, -40),
        (-20, -20),
        (-10, -20),
        (-10, 40),
        (10, 40),
        (10, -20),
    ]

    LEFT = [
        (-20, -40),
        (-40, -20),
        (-20, 0),
        (-20, -10),
        (0, -10),
        (0, 40),
        (20, 40),
        (20, -30),
        (-20, -30),
    ]

    RIGHT = [
        (20, -40),
        (40, -20),
        (20, 0),
        (20, -10),
        (0, -10),
        (0, 40),
        (-20, 40),
        (-20, -30),
        (20, -30),
    ]

    DOWN = [
        (20, 20),
        (0, 40),
        (-20, 20),
        (-10, 20),
        (-10, -40),
        (10, -40),
        (10, 20),
    ]


class Button:
    """This class defines an individual Button."""

    def __init__(self,
                 text,  # The text to display (can be None)
                 text_colour,  # The colour of the text/polygons (can be None)
                 background_colour,  # The colour of the text (can be None)
                 shape,  # string referring to name of Arrow Enum(can be None)
                 screen_location,  # The position on the screen
                 size):  # The size of the Button
        """Create a Button."""
        self.text = text
        self.text_colour = text_colour
        self.background_colour = background_colour
        self.shape = shape
        self.screen_location = screen_location
        self.size = size
        self.rect = pygame.Rect(screen_location, size)
        self.font = pygame.font.SysFont("comicsansms", 22)
        self.swapped = False  # Keeps track of wether a Button is swapped

        self.vertices = []
        enums = ['UP', 'LEFT', 'RIGHT', 'DOWN']
        for i in range(0, 4):
            if self.shape == enums[i]:
                self.vertices = self.get_vertex_list(
                    Arrow[enums[i]].value,
                    self.rect.centerx,
                    self.rect.centery,
                )

    def get_vertex_list(self, array, centerx, centery):
        """ Return usable list of vertices for pygame.draw.polygon """
        to_return = []
        # for each vector
        for i in range(0, len(array)):
            current = array[i]
            # append a vertex tuple to to_return
            to_return.append(
                (
                    current[0] + centerx,
                    current[1] + centery
                )
            )
        return to_return


    def display(self, screen):
        """Draw the Buttton object on screen, if it has a sprite."""
        # Draw the Button background
        screen.fill(self.background_colour, rect=self.rect)

        #if list of vectors is empty
        if self.vertices == []:
            # Draw the Button text
            text = self.font.render(self.text,
                                    True,
                                    self.text_colour)

            # Center the background and text
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.centery = self.rect.centery

            # Render Button on screen
            screen.blit(text, text_rect)

        else:
            pygame.draw.polygon(screen, self.text_colour, self.vertices)

    def swap_colours(self):
        """Swap the background and text / polygon colour of the Button."""
        temp_colour = self.text_colour
        self.text_colour = self.background_colour
        self.background_colour = temp_colour
        self.swapped = not self.swapped

    def is_mouse_over_button(self, mouse_position):
        """Given a mouse position, return True if mouse over Button."""
        return (mouse_position[0] > self.rect.topleft[0] and
                mouse_position[1] > self.rect.topleft[1] and
                mouse_position[0] < self.rect.bottomright[0] and
                mouse_position[1] < self.rect.bottomright[1])
