"""This file defines the ButtonGroup class."""


class ButtonGroup:
    """This class defines a store for all the Buttons used."""

    def __init__(self):
        """Create an empty ButtonGroup."""
        self.buttons = {}  # The underlying Button objects

    def add(self, button):
        """Add a Button to the ButtonGroup."""
        self.buttons[button.text] = button

    def display(self, screen):
        """Draw all Button objects in the ButtonGroup."""
        try:
            for _, button in self.buttons.items():
                button.display(screen)
        except:
            print("Runtime Error raised")
            pass

    def get_appropriate_button(self, mouse_position):
        """Return the pressed Button."""
        for _, button in self.buttons.items():
            if button.is_mouse_over_button(mouse_position):
                return button
        return None

    def unswap_all(self):
        """Unswap all Buttons where swapped equals True."""
        for _, button in self.buttons.items():
            if button.swapped:
                button.swap_colours()

    def removal_all(self):
        """Remove all Buttons from this ButtonGroup."""
        self.buttons = {}
