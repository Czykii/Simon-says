import pygame

class Button:
    def __init__(self, x, y, colour, size):
        self.x, self.y = x, y
        self.colour = colour
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.size, self.size))

    def clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.size and self.y <= mouse_y <= self.y + self.size
    
class Scores:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font_name = pygame.font.get_default_font()
        font = pygame.font.SysFont(font_name, 30)
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.x, self.y))

