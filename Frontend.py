import pygame

from Button import Button


class Drawer:
    def __init__(self, size, width=None, full_screen=False):
        pygame.init()
        self.size = size
        if width is None:
            self.screen_width = 500
        else:
            self.screen_width = width
        self.screen_height = int(9 / 9 * self.screen_width)
        if full_screen:
            # pass
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width = self.screen.get_rect().width
            self.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.CLOCK = pygame.time.Clock()

        pygame.display.set_caption("Tic Toe")

        self.light_blue = (0, 191, 255)
        self.grey = (204, 204, 204)
        self.blue = 33, 150, 243
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.light_red = (249, 76, 86)
        self.red = (255, 0, 0)
        self.bg_color = self.white

        self.button_bottom_color = self.black
        self.button_bottom_text = self.white
        self.button_bottom_height = 1.0 / 10.0 * self.screen_height

        self.button_color = self.blue
        self.button_color_lit = self.light_blue
        self.button_color_text = self.white

        self.line_color = self.black
        self.line_width = int(0.011 * self.screen_width)

        # setting fps manually
        self.fps = 60

        number_of_buttons_menu = 3
        menu_spacing = 0.1
        button_height = int(self.screen_height / (number_of_buttons_menu + (number_of_buttons_menu + 1) * menu_spacing))
        if button_height % 2 != 0:
            button_height -= 1
        screen_center = self.screen.get_rect().centerx

        coordinates_main_menu = []
        for i in range(number_of_buttons_menu):
            coordinates_main_menu.append((screen_center, (button_height * menu_spacing + button_height / 2) + (
                    button_height + button_height * menu_spacing) * i))

        button_size = (button_height, button_height)

        coordinates_menu_settings = []
        number_of_buttons_menu = 4
        button_height = int(self.screen_height / (number_of_buttons_menu + (number_of_buttons_menu + 1) * menu_spacing))
        if button_height % 2 != 0:
            button_height -= 1
        for i in range(number_of_buttons_menu):
            coordinates_menu_settings.append((screen_center, (button_height * menu_spacing + button_height / 2) + (
                    button_height + button_height * menu_spacing) * i))

        button_size_settings = (button_height, button_height)
        button_size_settings_small = (button_height / 2, button_height / 2)
        # self.button_size_small = (self.main_button_height / 2, self.main_button_height / 2)
        self.font_height = int(64 / 1080 * self.screen_height)
        font_height_small = int(self.font_height * 0.8)

        # this is used to track time

        transform_x = self.screen_width / self.size - 2 * self.line_width
        transform_y = (self.screen_height - self.button_bottom_height) / self.size - 2 * self.line_width
        # print(f"screen height: {self.screen_width}")
        # print(f"Transform x: {transform_x}")
        self.image_x = pygame.image.load("x_mine.png")
        self.image_x = pygame.transform.scale(self.image_x, (int(transform_x), int(transform_y)))
        # self.rect = self.image_x.get_rect()
        self.image_o = pygame.image.load("o_mine.png")
        self.image_o = pygame.transform.scale(self.image_o, (int(transform_x), int(transform_y)))

        # self.game_tic = TicToe()

        # Buttons

        # main menu
        self.start_button = Button(self, "START", coordinates_main_menu[0], button_size)
        self.settings_button = Button(self, "SETTINGS", coordinates_main_menu[1], button_size)
        self.quit_button = Button(self, "QUIT", coordinates_main_menu[2], button_size)
        # settings menu

        # first mode
        self.mode1_show_button = Button(self, "MODE HERE", coordinates_menu_settings[0], button_size_settings,
                                        font_size=font_height_small, button_color_lit=self.light_blue)
        top_left = self.mode1_show_button.rect.topleft
        self.change_mode1_button = Button(self, "FIRST PLAYER\nMODE", None,
                                          (button_size_settings[0], button_size_settings[1] * 1.2),
                                          font_size=font_height_small, button_color_lit=self.light_blue,
                                          topright=top_left)

        top_left = self.mode1_show_button.rect.topright
        self.difficulty_increase_button_1 = Button(self, "^", None, button_size_settings_small, topleft=top_left)
        bottom_left = self.mode1_show_button.rect.bottomright
        self.difficulty_decrease_button_1 = Button(self, "v", None, button_size_settings_small,
                                                   bottomleft=bottom_left)

        # second mode
        self.mode2_show_button = Button(self, "MODE HERE", coordinates_menu_settings[1], button_size_settings,
                                        font_size=font_height_small, button_color_lit=self.light_blue)
        top_left = self.mode2_show_button.rect.topleft
        self.change_mode2_button = Button(self, "SECOND\n PLAYER MODE", None,
                                          (button_size_settings[0], button_size_settings[1] * 1.2),
                                          font_size=font_height_small, button_color_lit=self.light_blue,
                                          topright=top_left)

        top_left = self.mode2_show_button.rect.topright
        self.difficulty_increase_button_2 = Button(self, "^", None, button_size_settings_small, topleft=top_left)

        top_left = self.difficulty_increase_button_2.rect.bottomleft
        self.difficulty_decrease_button_2 = Button(self, "v", None, button_size_settings_small, topleft=top_left)
        # change size of board
        self.size_show_button = Button(self, "SIZE DISPLAY HERE", coordinates_menu_settings[2],
                                       button_size_settings, font_size=font_height_small,
                                       button_color_lit=self.light_blue)
        top_left = self.size_show_button.rect.topleft
        self.size_text_button = Button(self, "BOARD SIZE:", None,
                                       (button_size_settings[0], button_size_settings[1] * 1.2),
                                       font_size=font_height_small, button_color_lit=self.light_blue,
                                       topright=top_left)

        top_left = self.size_show_button.rect.topright
        self.size_increase_button = Button(self, "^", None, button_size_settings_small, topleft=top_left)
        top_left = self.size_increase_button.rect.bottomleft
        self.size_decrease_button = Button(self, "v", None, button_size_settings_small, topleft=top_left)

        self.back_button = Button(self, "MENU", coordinates_menu_settings[3], button_size_settings)
        # game over menu
        self.play_again_button = Button(self, "PLAY AGAIN", coordinates_menu_settings[0], button_size_settings,
                                        font_size=font_height_small, button_color_lit=self.light_blue)

        self.over_back_button = Button(self, "MENU", coordinates_menu_settings[2], button_size_settings)

        # pause menu
        self.play_continue = Button(self, "CONTINUE", coordinates_menu_settings[0], button_size_settings,
                                    font_size=font_height_small, button_color_lit=self.light_blue)

    # updating board size
    def update_size(self, new_size):
        self.size = new_size
        transform_x = self.screen_width / self.size - 2 * self.line_width
        transform_y = (self.screen_height - self.button_bottom_height) / self.size - 2 * self.line_width
        self.image_x = pygame.image.load("x_mine.png")
        self.image_x = pygame.transform.scale(self.image_x, (int(transform_x), int(transform_y)))
        # self.rect = self.image_x.get_rect()
        self.image_o = pygame.image.load("o_mine.png")
        self.image_o = pygame.transform.scale(self.image_o, (int(transform_x), int(transform_y)))

    # managing displaying everything on screen
    def update_screen(self, board, message, coordinate_data, game_over=False, pause_menu=False):

        self.screen.fill(self.bg_color)

        self.draw_lines()

        self.draw_x_o(board)

        if coordinate_data[0] is not None:
            self.draw_winning_line(coordinate_data)

        self.draw_status(message)
        if game_over is True:
            self.print_game_over_menu()
        elif pause_menu is True:
            self.print_pause_menu()

        self.CLOCK.tick(self.fps)
        pygame.display.flip()

    # draw board lines
    def draw_lines(self):
        # drawing vertical lines

        for i in range(1, self.size):
            # draw vertical lines:
            pygame.draw.line(self.screen, self.black, (self.screen_width * i / self.size, 0),
                             (self.screen_width * i / self.size, self.screen_height - self.button_bottom_height),
                             self.line_width)
            # draw horizontal lines
            pygame.draw.line(self.screen, self.black,
                             (0, (self.screen_height - self.button_bottom_height) * i / self.size),
                             (self.screen_width, (self.screen_height - self.button_bottom_height) * i / self.size),
                             self.line_width)

    def draw_x_o(self, board):
        move = self.line_width
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == "X":
                    position_x = self.screen_width * j / self.size + move
                    position_y = (self.screen_height - self.button_bottom_height) * i / self.size + move
                    self.screen.blit(self.image_x, (position_x, position_y))
                elif board[i][j] == "O":
                    position_x = self.screen_width * j / self.size + move
                    position_y = (self.screen_height - self.button_bottom_height) * i / self.size + move
                    self.screen.blit(self.image_o, (position_x, position_y))

    # draw bottom status
    def draw_status(self, message):

        font = pygame.font.Font(None, self.font_height)

        # setting the font properties like
        # color and width of the text
        text = font.render(message, True, self.button_bottom_text)

        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        self.screen.fill(self.button_bottom_color,
                         (0, self.screen_height - self.button_bottom_height, self.screen_width, self.screen_height))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height - 0.5 * self.button_bottom_height))
        self.screen.blit(text, text_rect)
        # pygame.display.update()

    def draw_winning_line(self, coordinate_data):
        # coordinate_data - list. First index - what type of win. 0 - horizontal, 1 - vertical, 2 - crossing left
        # top, 3 - crossing right top
        # Second index - row or column or first index of crossing win.
        if coordinate_data[0] == 0:
            line_coordinates = (self.screen_height - self.button_bottom_height) * (2 * coordinate_data[1] + 1) / (
                    self.size * 2)
            pygame.draw.line(self.screen, self.red, (0, line_coordinates), (self.screen_width, line_coordinates),
                             self.line_width)
        elif coordinate_data[0] == 1:
            line_coordinates = self.screen_width * (2 * coordinate_data[1] + 1) / (self.size * 2)
            pygame.draw.line(self.screen, self.red, (line_coordinates, 0),
                             (line_coordinates, self.screen_height - self.button_bottom_height), self.line_width)
        elif coordinate_data[0] == 2:
            pygame.draw.line(self.screen, self.red, (0, 0),
                             (self.screen_width, (self.screen_height - self.button_bottom_height)), self.line_width)
        elif coordinate_data[0] == 3:
            pygame.draw.line(self.screen, self.red, (self.screen_width, 0),
                             (0, (self.screen_height - self.button_bottom_height)), self.line_width)

    def print_main_menu(self):
        self.screen.fill(self.bg_color)

        mouse_pos = pygame.mouse.get_pos()
        self.start_button.draw_button(mouse_pos)
        self.settings_button.draw_button(mouse_pos)
        self.quit_button.draw_button(mouse_pos)

        self.CLOCK.tick(self.fps)
        pygame.display.flip()

    def print_settings_menu(self, game_mode_1, game_mode_2, size):
        self.screen.fill(self.bg_color)

        mouse_pos = pygame.mouse.get_pos()

        self.change_mode1_button.draw_button(mouse_pos)
        self.mode1_show_button.draw_button(mouse_pos, new_msg=game_mode_1.upper())
        self.difficulty_increase_button_1.draw_button(mouse_pos)
        self.difficulty_decrease_button_1.draw_button(mouse_pos)

        self.change_mode2_button.draw_button(mouse_pos)
        self.mode2_show_button.draw_button(mouse_pos, new_msg=game_mode_2.upper())
        self.difficulty_increase_button_2.draw_button(mouse_pos)
        self.difficulty_decrease_button_2.draw_button(mouse_pos)

        self.size_text_button.draw_button(mouse_pos)
        self.size_show_button.draw_button(mouse_pos, new_msg=str(size))
        self.size_increase_button.draw_button(mouse_pos)
        self.size_decrease_button.draw_button(mouse_pos)

        self.back_button.draw_button(mouse_pos)

        self.CLOCK.tick(self.fps)
        pygame.display.flip()

    def print_game_over_menu(self):

        mouse_pos = pygame.mouse.get_pos()
        self.play_again_button.draw_button(mouse_pos)
        self.over_back_button.draw_button(mouse_pos)

    def print_pause_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        self.play_continue.draw_button(mouse_pos)
        self.over_back_button.draw_button(mouse_pos)

    # not used yet
    def change_resolution(self, width):
        self.__init__(self.size, width)
