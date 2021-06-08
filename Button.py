import pygame.font


class Button:
    def __init__(self, game, msg, position, size, font_size=None, button_color=None, button_color_lit=None,
                 topleft=None, topright=None, bottomleft=None):

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.height = size[0]
        self.width = size[1]
        if font_size is None:
            self.button_font_height = game.font_height
        else:
            self.button_font_height = font_size
        self.text_color = game.button_color_text

        self.font = pygame.font.SysFont("", self.button_font_height)

        # Build the button's rect object and adjust it position.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        if topleft:
            self.rect.topleft = topleft
        elif topright:
            self.rect.topright = topright
        elif bottomleft:
            self.rect.bottomleft = bottomleft
        else:
            self.rect.center = position

        self.msg = msg
        if button_color is None:
            self.button_color_normal = game.button_color
            self.button_color = game.button_color
        else:
            self.button_color_normal = button_color
            self.button_color = button_color
        if button_color_lit is None:
            self.button_color_lit = game.button_color_lit
        else:
            self.button_color_lit = button_color_lit

    def _prep_msg(self, multiline=None, position=None):
        if multiline is None:
            message = self.msg
            self.msg_image = self.font.render(message, True, self.text_color, self.button_color)
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.rect.center
        else:
            message = multiline
            self.msg_image = self.font.render(message, True, self.text_color, self.button_color)
            self.msg_image_rect = self.msg_image.get_rect()

            temporary = tuple(map(sum, zip(self.rect.midtop, (0, (position + 1.5) * self.button_font_height))))
            self.msg_image_rect.center = temporary

    def draw_button(self, mouse_pos, new_msg=None):

        if self.rect.collidepoint(mouse_pos):
            self.button_color = self.button_color_lit
        else:
            self.button_color = self.button_color_normal
        if new_msg is not None:
            self.msg = new_msg

        self.screen.fill(self.button_color, self.rect)
        if "\n" in self.msg:
            lines_split = self.msg.split("\n")
            for index, line in enumerate(lines_split):
                self._prep_msg(multiline=line, position=index)
                self.screen.blit(self.msg_image, self.msg_image_rect)
        else:
            self._prep_msg()
            self.screen.blit(self.msg_image, self.msg_image_rect)
