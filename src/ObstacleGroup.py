"""This file defines the ObstacleGroup class."""


class ObstacleGroup:
    """This class defines a store for all the goals used."""

    def __init__(self):
        """Create an empty ObstacleGroup."""
        self.obstacles = []  # The underlying Goal objects

    def add(self, obstacle):
        """Add a Obstacle to the ObstacleGroup."""
        self.obstacles.append(obstacle)

    def display(self, screen):
        """Draw all Obstacle objects in the ObstacleGroup."""
        for obstacle in self.obstacles:
            obstacle.display(screen)
