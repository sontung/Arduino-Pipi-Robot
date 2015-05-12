import pygame
import sys
import core_communication
from pygame.locals import *


class JoystickInfo:
    def __init__(self):
        self.axis_to_command = {
            2: 1.0,
            4: -1.0,
            6: 1.0,
            8: -1.0
        }

        joystick_count = pygame.joystick.get_count()

        # For each joystick:
        for i in range(joystick_count):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()

            # Get the name from the OS for the controller/joystick
            self.name = self.joystick.get_name()

    def get_axes_val(self):
        """
        Get axis values from the joystick.
        :return:
        """
        axes1 = []
        axes2 = []
        num_axes = self.joystick.get_numaxes()
        for i in range(num_axes):
            if i <= 1:
                axes1.append(self.joystick.get_axis(i))
            elif i <= 3:
                axes2.append(self.joystick.get_axis(i))
        return axes1, axes2

    def if_move(self, type):
        """
        Sense the motion of the joystick.
        :param type:
        :return:
        """
        if type == "axis":
            val1, val2 = self.get_axes_val()
            for x in val1:
                if abs(x) == 1.0:
                    return "1"
            for y in val2:
                if abs(y) == 1.0:
                    return "2"
            return None

    def interpret(self, type):
        """
        Interpret input values from the joystick into
        commands.
        :return:
        """
        if type == "axis":
            val1, val2 = self.get_axes_val()
            motion = self.if_move(type)
            print motion
            if motion is not None:
                if motion == "1":
                    if abs(val1[0]) == 1:
                        if self.axis_to_command[4] == val1[0]:
                            return 4
                        elif self.axis_to_command[6] == val1[0]:
                            return 6
                    elif abs(val1[1]) == 1:
                        if self.axis_to_command[2] == val1[1]:
                            return 2
                        elif self.axis_to_command[8] == val1[1]:
                            return 8
                elif motion == "2":
                    if abs(val2[0]) == 1:
                        if self.axis_to_command[4] == val2[0]:
                            return 4
                        elif self.axis_to_command[6] == val2[0]:
                            return 6
                    if abs(val2[1]) == 1:
                        if self.axis_to_command[2] == val2[1]:
                            return 2
                        elif self.axis_to_command[8] == val2[1]:
                            return 8


class EventLogic:
    def __init__(self, _game_state, _game_gui):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self.bluetooth_talk = core_communication.Communication()
        #self.joystick_tracking = JoystickInfo()
        self.movement = {
            K_UP: 8,
            K_DOWN: 2,
            K_RIGHT: 6,
            K_LEFT: 4
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
                if self._game_gui.back.get_rect().collidepoint(event.pos):
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

        elif event.type == JOYAXISMOTION:
            if self._game_state.get_state() == "new season":
                while self.joystick_tracking.if_move("axis") is not None:
                    self._game_gui.modify_pos_pad(self.joystick_tracking.interpret("axis"))
                    self.bluetooth_talk.command(str(self.joystick_tracking.interpret("axis")))
                    self.event_handler()

        elif event.type == KEYUP: #or self.joystick_tracking.if_move("axis") is None:
            if self._game_state.get_state() == "new season":
                self.bluetooth_talk.command('0')
                self._game_gui.modify_pos_pad(0)

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.quit()

            elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                if self._game_state.get_state() == "new season":
                    while pygame.key.get_pressed()[event.key]:
                        self._game_gui.modify_pos_pad(self.movement[event.key])
                        self.bluetooth_talk.command(str(self.movement[event.key]))
                        self.event_handler()

            if self._game_gui.typing_tag:
                if event.key in range(48, 58) or event.key in range(256, 266):
                    if event.key < 100:
                        char = str(event.key-48)
                    elif event.key < 300:
                        char = str(event.key-256)
                    self._game_gui.prompt.take_char(char)

                elif event.key == K_BACKSPACE:
                    self._game_gui.prompt.take_char("del")