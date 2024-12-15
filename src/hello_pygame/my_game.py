import time

import pygame
from py_app_dev.core.logging import logger


class MyGame:
    """
    A simple PyGame-based application that displays circles on the screen where the user clicks, and shows the number of clicks at the top-right corner.

    The circles remain visible for a limited lifetime. Right-clicking resets the state.
    """

    def __init__(self, width: int = 800, height: int = 600, circle_lifetime: float = 3.0) -> None:
        """
        Initialize the MyGame application.

        :param width: The width of the PyGame window in pixels.
        :param height: The height of the PyGame window in pixels.
        :param circle_lifetime: The number of seconds a circle remains visible.
        """
        self.logger = logger.bind()
        self.width = width
        self.height = height
        self.circle_lifetime = circle_lifetime

        # Initialize pygame and create a window
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PyGame Circle Click Example")

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 24)

        # Track all clicks as a list of tuples: (x: int, y: int, timestamp: float)
        self.clicks: list[tuple[int, int, float]] = []
        self.click_count: int = 0

        # Define colors
        self.bg_color: tuple[int, int, int] = (30, 30, 30)  # Dark background
        self.text_color: tuple[int, int, int] = (255, 255, 255)  # White text
        self.circle_color: tuple[int, int, int] = (255, 0, 0)  # Red circle

        self.running: bool = True

    def run(self) -> None:
        """Run the main event loop of the game until a quit event is encountered. Handles user input, updates game state, and renders the scene."""
        self.logger.info(f"Running {self.__class__.__name__}")

        clock = pygame.time.Clock()

        while self.running:
            # Handle events such as quitting, left-clicking, and right-clicking.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Left click: record the click
                        x, y = event.pos
                        self.clicks.append((x, y, time.time()))
                        self.click_count += 1
                        self.logger.info(f"Left click registered at: ({x}, {y})")
                    elif event.button == 3:
                        # Right click: reset the game state
                        self.clicks.clear()
                        self.click_count = 0
                        self.logger.info("Right click detected, state reset.")

            # Update the list of circles to remove those whose lifetime has expired.
            self._update_circles()

            # Draw the current frame.
            self._draw()

            # Limit the frame rate to 60 FPS.
            clock.tick(60)

        pygame.quit()

    def _update_circles(self) -> None:
        """Update the state of circles, removing any that have exceeded their lifetime."""
        current_time = time.time()
        self.clicks = [(x, y, t) for (x, y, t) in self.clicks if current_time - t < self.circle_lifetime]

    def _draw(self) -> None:
        """Render the current game state to the screen, including the background, active circles, and click count text."""
        # Fill the background
        self.screen.fill(self.bg_color)

        # Draw each circle
        for x, y, _ in self.clicks:
            pygame.draw.circle(self.screen, self.circle_color, (x, y), 20)

        # Render click count in the upper-right corner
        click_text = self.font.render(f"Clicks: {self.click_count}", True, self.text_color)
        text_rect = click_text.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(click_text, text_rect)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    game = MyGame()
    game.run()
