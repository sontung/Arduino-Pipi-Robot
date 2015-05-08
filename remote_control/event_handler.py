import pygame
import sys
import core_communication
from pygame.locals import *


class EventLogic:
    def __init__(self, _game_state, _game_gui):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self.bluetooth_talk = core_communication.Communication()
        self.movement = {
            K_UP: "up",
            K_DOWN: "down",
            K_RIGHT: "right",
            K_LEFT: "left"
        }

    def quit(self):
        pygame.quit()
        sys.exit()

    def event_handler(self):

        event = pygame.event.poll()
        if event.type == MOUSEBUTTONUP:
            if self._game_state.get_state() == "welcome":
                if self._game_gui.new.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new season")
                    if self.bluetooth_talk.serial_port is None:
                        self._game_state.set_state("error")
                    else:
                        try:
                            self.bluetooth_talk.connect()
                        except IOError:
                            self._game_state.set_state("error")
                elif self._game_gui.help.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("help")
                elif self._game_gui.author.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("author")
                elif self._game_gui.setting.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("setting")
                elif self._game_gui.quit.get_rect().collidepoint(event.pos):
                    self.quit()
            elif self._game_state.get_state() == "new season":
                if self._game_gui.zero.get_rect().collidepoint(event.pos):
                    self.bluetooth_talk.write("0")
                    print "sending 0"
                elif self._game_gui.one.get_rect().collidepoint(event.pos):
                    self.bluetooth_talk.write("1")
                    print "sending 1"
                elif self._game_gui.back.get_rect().collidepoint(event.pos):
                    self.bluetooth_talk.disconnect()
                    self._game_state.set_state("welcome")
            elif self._game_state.get_state() == "setting":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
                elif self._game_gui.prompt_rect.collidepoint(event.pos):
                    self._game_gui.set_typing_tag(True)
                elif self._game_gui.save.get_rect().collidepoint(event.pos):
                    self.bluetooth_talk.specify_port(int(self._game_gui.prompt.output()[0]))
                    self._game_gui.prompt.reset()
                else:
                    self._game_gui.set_typing_tag(False)
            elif self._game_state.get_state() == "error":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
            elif self._game_state.get_state() in ["help", "author", "setting"]:
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")

        elif event.type == MOUSEMOTION or event.type == NOEVENT:
            if self._game_gui.buttons:
                self._game_gui.draw(self._game_state.get_state())
                for button in self._game_gui.buttons:
                    button.set_bold(pygame.mouse.get_pos())
                pygame.display.update()

        elif event.type == pygame.QUIT:
            self.quit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.quit()

            elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                if self._game_state.get_state() == "new season":
                    pass

            if self._game_gui.typing_tag:
                if event.key in range(48, 58) or event.key in range(256, 266):
                    if event.key < 100:
                        char = str(event.key-48)
                    elif event.key < 300:
                        char = str(event.key-256)
                    self._game_gui.prompt.take_char(char)

                elif event.key == K_BACKSPACE:
                    self._game_gui.prompt.take_char("del")