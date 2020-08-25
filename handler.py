
from object import *
from my_functions import *

class Handler:
    def __init__(self):
        pygame.init()
        logo = pygame.image.load("resources/rat_idle.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("LONGEVITY")
        self.screen = pygame.display.set_mode((1280,720))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()

        self.SCREEN_W = 1280
        self.SCREEN_H = 720

        self.running = False
        self.next_screen = pygame.Surface((self.SCREEN_W, self.SCREEN_H))

        self.my_objects = []
        self.avatar = 0
        self.playing = True

        self.small_font = pygame.font.Font('freesansbold.ttf', 32)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 54)
        self.large_font = pygame.font.Font('freesansbold.ttf', 86)

        #self.AVATAR_ATTACK_END = pygame.USEREVENT + 1 #reserved for attack animation

        self.backgrounds = []
        self.backgrounds.append(pygame.image.load("resources/main_menu_bg.png"))
        self.fader = pygame.Surface((self.SCREEN_W, self.SCREEN_H))
        self.fader.fill((0,0,0))
        self.fader_alpha = 0
        self.fading = False



        self.number_of_deaths = 0
        #Try to load config info
        try:
            dataFile = open("resources/game_config.txt", "r")
            rawLines = dataFile.readlines()
            self.number_of_deaths = int(rawLines[0])
            dataFile.close()
        except FileNotFoundError:
            self.number_of_deaths = 0

        start_game_msg = "START THE" + num2ordinal(self.number_of_deaths + 1).upper() + " GAME"
        self.cemetery_bg = pygame.image.load("resources/cemetery_" + str(self.number_of_deaths) + ".png")
        self.cemetery_lamp = pygame.image.load("resources/lamp_extended.png").convert_alpha()

        main_menu_result = self.menu_window("", [start_game_msg, "OPTIONS", "ACHIEVEMENTS"], 0, 400)
        if main_menu_result == 0:
            self.start_game()

    def add_object(self, new_object):
        self.my_objects.append(new_object)

    def set_avatar(self, object):
        self.avatar = object

    def fade_out(self):
        self.fading = True
        self.fader_alpha = 0

    def print_text(self, my_text, pos_x, pos_y, size=0, text_color = (255, 255, 255)):
        if size == 0:
            text = self.small_font.render(my_text, True, text_color, (0, 0, 0))
        if size == 1:
            text = self.medium_font.render(my_text, True, text_color, (0,0,0))
        if size == 2:
            text = self.large_font.render(my_text, True, text_color, (0,0,0))

        if pos_x == "center":
            if pos_y == "center":
                self.screen.blit(text, (self.SCREEN_W / 2 - text.get_rect().width / 2, self.SCREEN_H / 2 - text.get_rect().height / 2))
            else:
                self.screen.blit(text, (self.SCREEN_W / 2 - text.get_rect().width / 2, pos_y))
        else:
            if pos_y == "center":
                self.screen.blit(text, (pos_x, self.SCREEN_H / 2 - text.get_rect().height / 2))
            else:
                self.screen.blit(text, (pos_x, pos_y))
        #self.screen.blit(text, (pos_x, pos_y))
        pygame.display.flip()

    def menu_window(self, my_text, options, bg = 0, y_0 = 300):
        self.print_text(my_text, "center", 150, 0, (255, 255, 255))

        texts = []
        #y_0 = 300
        cur_y = y_0
        selected_option = 0

        button_width = 500

        self.screen.blit(self.backgrounds[bg], (0, 0))

        for i in range(len(options)):
            option = options[i]
            if(i != selected_option):
                texts.append(self.small_font.render(option, True, (255, 255, 255), (0, 0, 0)))
                pygame.draw.rect(self.screen, (255, 255, 255), (self.SCREEN_W / 2 - button_width / 2, cur_y - 10, button_width, texts[-1].get_rect().height + 20), 1)
            else:
                texts.append(self.small_font.render(option, True, (0, 0, 0), (255, 255, 255)))
                pygame.draw.rect(self.screen, (255, 255, 255), (self.SCREEN_W / 2 - button_width / 2, cur_y - 10, button_width, texts[-1].get_rect().height + 20))
            self.screen.blit(texts[-1], (self.SCREEN_W / 2 - texts[-1].get_rect().width / 2, cur_y))
            cur_y += 70

        pygame.display.flip()

        waiting = True

        while(waiting):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        return(selected_option)
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        return(selected_option)
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                        self.screen.blit(self.backgrounds[bg], (0, 0))
                        pygame.draw.rect(self.screen, (0,0,0), (self.SCREEN_W / 2 - button_width / 2 - 1, y_0-11, button_width + 2, self.SCREEN_H))
                        texts = []
                        cur_y = y_0

                        for i in range(len(options)):
                            option = options[i]
                            if(i != selected_option):
                                texts.append(self.small_font.render(option, True, (255, 255, 255), (0, 0, 0)))
                                pygame.draw.rect(self.screen, (255, 255, 255), (self.SCREEN_W / 2 - button_width / 2, cur_y - 10, button_width, texts[-1].get_rect().height + 20), 1)
                            else:
                                texts.append(self.small_font.render(option, True, (0, 0, 0), (255, 255, 255)))
                                pygame.draw.rect(self.screen, (255, 255, 255), (self.SCREEN_W / 2 - button_width / 2, cur_y - 10, button_width, texts[-1].get_rect().height + 20))
                            self.screen.blit(texts[-1], (self.SCREEN_W / 2 - texts[-1].get_rect().width / 2, cur_y))
                            cur_y += 70

                        pygame.display.flip()
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                        self.screen.blit(self.backgrounds[bg], (0, 0))
                        pygame.draw.rect(self.screen, (0,0,0), (self.SCREEN_W / 2 - button_width / 2 - 1, y_0-11, button_width + 2, self.SCREEN_H))
                        texts = []
                        cur_y = y_0

                        for i in range(len(options)):
                            option = options[i]
                            if(i != selected_option):
                                texts.append(self.small_font.render(option, True, (255, 255, 255), (0, 0, 0)))
                                pygame.draw.rect(self.screen, (255, 255, 255), (self.SCREEN_W / 2 - button_width / 2, cur_y - 10, button_width, texts[-1].get_rect().height + 20), 1)
                            else:
                                texts.append(self.small_font.render(option, True, (0, 0, 0), (255, 255, 255)))
                                pygame.draw.rect(self.screen, (255, 255, 255), (self.SCREEN_W / 2 - button_width / 2, cur_y - 10, button_width, texts[-1].get_rect().height + 20))
                            self.screen.blit(texts[-1], (self.SCREEN_W / 2 - texts[-1].get_rect().width / 2, cur_y))
                            cur_y += 70

                        pygame.display.flip()
        self.screen.fill((0,0,0))

    def start_game(self):
        #Fade out from the menu
        for i in range(5):
            self.clock.tick(2) #FPS
            self.fader.set_alpha(45 * (i + 1))
            self.screen.blit(self.fader, (0, 0))
            pygame.display.flip()
        self.clock.tick(1)
        for i in range(21):
            self.screen.blit(self.cemetery_bg, (0, 0))
            self.screen.blit(self.cemetery_lamp, (-1280 + i * 64, -90))
            pygame.display.flip()
            self.clock.tick(2)
