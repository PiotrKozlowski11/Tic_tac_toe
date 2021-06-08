import logging
import sys
# import time

import pygame

from Frontend import Drawer
from Backend import TicToe

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s- %(message)s")

# logging.disable(logging.CRITICAL)


class Merged:
    def __init__(self):
        # default size when launching game
        self.size = 3
        # backend calculations
        self.back = None
        # frontend - pygame
        self.front = Drawer(self.size)

        # default game difficulties
        self.game_mode_1 = "user"
        self.game_mode_2 = "medium"

        # list of available difficulties
        self.game_modes_list = ["user", "easy", "medium", "hard"]
        self.game_modes = (self.game_mode_1, self.game_mode_2)
        self.mode_index = 0
        self.current_mode = self.game_modes[self.mode_index]

        # field used to choose field when it's user move
        self.choose_field = False

        # game is running
        self.game_status_play = False
        # game is over
        self.game_status_over = False

        # main menu is active
        self.game_main_menu = True
        # settings menu is active
        self.game_settings_menu = False
        # pause menu is active
        self.pause_menu = False
        # message displayed at bottom
        self.message = ""

    # method used to run whole game
    def run_everything(self):
        while True:
            # handling main menu and settings menu
            if self.game_main_menu:
                self.check_events()
                if self.game_settings_menu is True:
                    self.front.print_settings_menu(self.game_mode_1, self.game_mode_2, self.size)
                else:
                    self.front.print_main_menu()
            # handling main game
            elif self.game_status_play:

                self.prepare_msg()
                self.front.update_screen(self.back.board, self.message, self.back.win_coordinates)
                # different modes and difficulties
                if self.current_mode == "user":
                    self.choose_field = True
                elif self.current_mode == "easy":
                    # time.sleep(0.5)
                    self.back.easy_mode()
                    self.back.reverse_symbol()
                    self.switch_mode()
                elif self.current_mode == "medium":
                    # time.sleep(0.5)
                    self.back.medium_mode()
                    self.back.reverse_symbol()
                    self.switch_mode()
                elif self.current_mode == "hard":
                    # time.sleep(0.5)
                    self.back.hard_mode()
                    self.back.reverse_symbol()
                    self.switch_mode()
                # checking if sb won
                self.check_events()
                self.back.check_win()

                # logging.debug(self.back.game_status)

                # if sb won : switch current symbol (used if user will play again - to start with same symbol selected)
                # set status of active game to False and game over to True
                if self.back.game_status:
                    self.switch_mode()
                    self.game_status_play = False
                    self.game_status_over = True
            # if game is over print line matching won fields and display game over menu
            elif self.game_status_over:
                self.prepare_msg()
                self.front.update_screen(self.back.board, self.message, self.back.win_coordinates, game_over=True)
                self.check_events()
            # display and handle pause menu
            elif self.pause_menu:
                # print("pause menu")
                self.prepare_msg()
                self.front.update_screen(self.back.board, self.message, self.back.win_coordinates, pause_menu=True)
                self.check_events()
            # self.check_events()

    # switching current mode of game (e.g. from "user" to "medium")
    def switch_mode(self):
        if self.mode_index == 0:
            self.mode_index = 1
        else:
            self.mode_index = 0
        self.current_mode = self.game_modes[self.mode_index]

    # preparing message displayed at bottom of screen
    def prepare_msg(self):
        if self.back.game_status is None:
            self.message = self.back.symbol + "'s Turn"
        elif self.back.game_status == "_":
            self.message = "Draw"
        elif self.back.game_status != "_":
            self.message = "{} wins".format(self.back.game_status)
        else:
            print("error")

    # checking all events of game - including event in all menus
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # mouse clicking
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # if it's user's turn to select field when game is running
                if self.choose_field is True:
                    logging.debug(self.back.board)
                    # checking which field was selected
                    move = self.check_mouse_position(mouse_pos)
                    # checking if field is occupied
                    move_result = self.back.check_move(move)
                    # if not - user cannot longer select fields, reverse current symbol (e.g. from "O" to "X") and
                    # switch current mode
                    if move_result:
                        self.choose_field = False
                        self.back.reverse_symbol()
                        self.switch_mode()
                # handle mouse down when it's main menu or game over or pause menu
                elif self.game_main_menu is True or self.game_status_over is True or self.pause_menu:
                    self.check_mouse_position_main_menu(mouse_pos)
            # activate pause menu by escape key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.game_main_menu is False:

                    if self.pause_menu is True:
                        # self.choose_field = False
                        self.pause_menu = False
                        self.game_status_play = True
                    else:
                        self.choose_field = False
                        self.pause_menu = True
                        self.game_status_play = False

    # checking mouse position when game is running and returning currently selected field
    def check_mouse_position(self, mouse_pos):
        x, y = mouse_pos
        column = None
        row = None
        for i in range(1, self.back.size + 1):
            if x / self.front.screen_width < i / self.back.size:
                column = i - 1
                break
        for i in range(1, self.back.size + 1):
            if y / (self.front.screen_height - self.front.button_bottom_height) < i / self.back.size:
                row = i - 1
                break

        if column is None or row is None:
            return None

        return [row, column]

    # handling mouse down button when it's main menu
    def check_mouse_position_main_menu(self, mouse_pos):
        # settings menu
        if self.game_settings_menu:
            self.handle_settings_menu(mouse_pos)
        # game over menu
        elif self.game_status_over:
            button_clicked_play_again = self.front.play_again_button.rect.collidepoint(mouse_pos)
            button_clicked_menu = self.front.over_back_button.rect.collidepoint(mouse_pos)
            if button_clicked_play_again:
                self.back = TicToe(self.size)
                self.mode_index = 0
                self.current_mode = self.game_modes[self.mode_index]
                self.game_main_menu = False
                self.game_status_play = True
                self.game_status_over = False
                self.pause_menu = False
            elif button_clicked_menu:
                self.game_status_over = False
                self.game_main_menu = True
        # main menu
        elif self.game_main_menu:
            button_clicked_play = self.front.start_button.rect.collidepoint(mouse_pos)
            button_clicked_settings = self.front.settings_button.rect.collidepoint(mouse_pos)
            button_clicked_quit = self.front.quit_button.rect.collidepoint(mouse_pos)
            if button_clicked_play:
                self.back = TicToe(self.size)
                self.mode_index = 0
                self.current_mode = self.game_modes[self.mode_index]
                self.game_status_play = True
                self.game_main_menu = False
            elif button_clicked_settings:
                # self.front.change_resolution(self.front.screen_width+100)
                # self.front = Drawer(self.size, full_screen=True)
                self.game_settings_menu = True
            elif button_clicked_quit:
                sys.exit()
        elif self.pause_menu:
            button_clicked_play_continue = self.front.play_continue.rect.collidepoint(mouse_pos)
            button_clicked_menu = self.front.over_back_button.rect.collidepoint(mouse_pos)
            if button_clicked_play_continue:
                self.pause_menu = False
                self.game_status_play = True
            elif button_clicked_menu:
                self.game_status_over = False
                self.game_main_menu = True
                self.pause_menu = False

    # handling settings menu
    def handle_settings_menu(self, mouse_pos):
        # all possible buttons which can be selected
        button_clicked_back = self.front.back_button.rect.collidepoint(mouse_pos)

        button_clicked_increase_mode_1 = self.front.difficulty_increase_button_1.rect.collidepoint(mouse_pos)
        button_clicked_decrease_mode_1 = self.front.difficulty_decrease_button_1.rect.collidepoint(mouse_pos)

        button_clicked_increase_mode_2 = self.front.difficulty_increase_button_2.rect.collidepoint(mouse_pos)
        button_clicked_decrease_mode_2 = self.front.difficulty_decrease_button_2.rect.collidepoint(mouse_pos)

        button_clicked_increase_size = self.front.size_increase_button.rect.collidepoint(mouse_pos)
        button_clicked_decrease_size = self.front.size_decrease_button.rect.collidepoint(mouse_pos)

        if button_clicked_back:
            self.game_modes = (self.game_mode_1, self.game_mode_2)
            self.mode_index = 0
            self.current_mode = self.game_modes[self.mode_index]
            self.game_settings_menu = False

        elif button_clicked_increase_mode_1:
            temporary = self.game_modes_list.index(self.game_mode_1) + 1
            if temporary > len(self.game_modes_list) - 1:
                temporary = 0
            self.game_mode_1 = self.game_modes_list[temporary]
            self.game_modes = (self.game_mode_1, self.game_mode_2)

        elif button_clicked_decrease_mode_1:
            temporary = self.game_modes_list.index(self.game_mode_1) - 1
            if temporary < 0:
                temporary = len(self.game_modes_list) - 1
            self.game_mode_1 = self.game_modes_list[temporary]
            self.game_modes = (self.game_mode_1, self.game_mode_2)

        elif button_clicked_increase_mode_2:
            temporary = self.game_modes_list.index(self.game_mode_2) + 1
            if temporary > len(self.game_modes_list) - 1:
                temporary = 0
            self.game_mode_2 = self.game_modes_list[temporary]
            self.game_modes = (self.game_mode_1, self.game_mode_2)

        elif button_clicked_decrease_mode_2:
            temporary = self.game_modes_list.index(self.game_mode_2) - 1
            if temporary < 0:
                temporary = len(self.game_modes_list) - 1
            self.game_mode_2 = self.game_modes_list[temporary]
            self.game_modes = (self.game_mode_1, self.game_mode_2)

        # increasing size of board
        # if board is single field is too small or too big in order to be displayed - handle ZeroDivision or Value Error
        elif button_clicked_increase_size:
            try:
                temp_size = self.size + 1
                self.front.update_size(temp_size)
                self.size = temp_size
            except ZeroDivisionError:
                self.front.update_size(self.size)
            except ValueError:
                self.front.update_size(self.size)

        elif button_clicked_decrease_size:
            try:
                temp_size = self.size - 1
                self.front.update_size(temp_size)
                self.size = temp_size
            except ZeroDivisionError:
                self.front.update_size(self.size)
            except ValueError:
                self.front.update_size(self.size)

        if "hard" in self.game_modes:
            if self.size > 6:
                self.size = 6
                self.front.update_size(self.size)


if __name__ == "__main__":
    logging.debug("Start of program")

    run_sth = Merged()
    run_sth.run_everything()

    logging.debug("End of program")
