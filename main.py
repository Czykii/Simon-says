import json
import random
from button import *

class Game:
    def __init__(self, data):
        self.data = data
        pygame.init()
        self.screen = pygame.display.set_mode((self.data["width"], self.data["width"]))
        pygame.display.set_caption(self.data["name"])
        self.clock = pygame.time.Clock()
        self.flash_colour = self.data["colours"]["BLUE"]
        self.colour = self.data["colours"]["LIGHTGREY"]

        self.buttons = []
        
        start_y = 100
        for _ in range(3):
            start_x = 100
            for _ in range(3):    
               button = Button(start_x, start_y, self.colour, self.data["button_size"])
               self.buttons.append(button)
               start_x += self.data["button_size"] + 10
            start_y += self.data["button_size"] + 10
    
    def get_high_score(self):
        with open("high_score.txt", "r") as input:
            score = input.read()
        return int(score)
    
    def set_high_score(self):
        with open("high_score.txt", "w") as output:
            if self.score > self.high_score:
                output.write(str(self.score))
            else:
                output.write(str(self.high_score))
    
    def new(self):
        self.waiting_input = False
        self.pattern = []
        self.step = 0
        self.score = 0
        self.high_score = self.get_high_score()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(self.data["fps"])
            self.clicked_button = None
            self.events()
            self.draw()
            self.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.clicked(mouse_x, mouse_y):
                        self.clicked_button = button

    def draw(self):
        self.screen.fill(self.data["colours"]["GREY"])
        Scores(250, 40, f"Score: {str(self.score)}").draw(self.screen)
        Scores(450, 40, f"High score: {str(self.high_score)}").draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()

    def update(self):
        if not self.waiting_input:
            pygame.time.wait(1000)
            self.pattern.append(random.choice(self.buttons))
            for button in self.pattern:
                self.button_animation(button)
                pygame.time.wait(200)
            self.waiting_input = True
        
        else:
            if self.clicked_button and self.clicked_button == self.pattern[self.step]:
                self.button_animation(self.clicked_button)
                self.step += 1

                if self.step == len(self.pattern):
                    self.score += 1
                    self.waiting_input = False
                    self.step = 0
            elif self.clicked_button and self.clicked_button != self.pattern[self.step]:
                    self.playing = False
                    self.game_over_animation()
                    self.set_high_score()

    def button_animation(self, button):
        button = button
        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((self.data["button_size"], self.data["button_size"]))
        flash_surface = flash_surface.convert_alpha()
        r, g, b = self.flash_colour
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, self.data["animation_speed"] * step):
                self.screen.blit(original_surface, (0, 0))
                flash_surface.fill((r, g, b, alpha))
                self.screen.blit(flash_surface, (button.x, button.y))
                pygame.display.update()
                self.clock.tick(self.data["fps"])
        self.screen.blit(original_surface, (0, 0))

    def game_over_animation(self):
        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((self.screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
        r, g, b = self.data["colours"]["WHITE"]
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, self.data["animation_speed"] * step):
                    self.screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    self.screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    self.clock.tick(self.data["fps"])


def main():
    with open('settings.json') as config_file:
            data = json.load(config_file)
    game = Game(data)
    while True:
        game.new()
        game.run()    

main()