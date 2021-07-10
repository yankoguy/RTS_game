import pygame as pg
from camera import cam_values
from settings import *


class Mouse:
    CLICK_STATE = 0
    CLICK_RELESE_STATE = 1
    DOUBLE_CLICK_STATE = 2
    HOLD_STATE = 3

    def __init__(self):
        self.cursor = None

        self.start_selcet_area = (0, 0)
        self.end_selcet_area = (0, 0)
        self.agent_to_activate = 0

        self.state = Mouse.CLICK_STATE

        self.handler_functions = {pg.MOUSEBUTTONDOWN: self.mouse_click,
                                  pg.MOUSEBUTTONUP: self.mouse_up}

    def mouse_event_handler(self, event_type, func_to_activate, *additional):
        self.handler_functions[event_type](func_to_activate,additional)

    def update(self):

        if self.state == Mouse.HOLD_STATE:
            self.end_selcet_area = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

    def create_cursor_image(self, cursor_image):
        if self.cursor is None:
            self.cursor = cursor_image

    def mouse_click(self, func_to_activate, args):
        """function that runs every left click on the mouse"""
        # if not self.drag:
        #   self.cursor = None

        if self.state != Mouse.HOLD_STATE:
            self.start_hold()

        args = pg.mouse.get_pos() + args
        func_to_activate(*args)  # add cheks

    def start_hold(self):
        self.state = Mouse.HOLD_STATE  # start select mode until mouse is not preesed
        self.start_selcet_area = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        self.end_selcet_area = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

        """
        if self.agent_to_activate:
            # activate agents which were in block
            for agent in self.agent_to_activate:
                target_x = pg.mouse.get_pos()[0] / cam_values.tile_size - cam_values.x
                target_y = pg.mouse.get_pos()[1] / cam_values.tile_size - cam_values.y - 5
                target_type = click_info_func(int(target_x / TILE_SIZE), int(target_y / TILE_SIZE))
                agent.prepare_agent((target_x, target_y), target_type)

            self.agent_to_activate = []
        """

    def mouse_up(self, func_to_activate, args):
        if self.state == Mouse.HOLD_STATE:
            self.end_hold()

        if self.state == Mouse.HOLD_STATE:
            func_to_activate(*args,self.start_selcet_area,self.end_selcet_area)  # add cheks
        else:
            func_to_activate(*args)  # add cheks

        self.start_selcet_area = (0, 0)
        self.end_selcet_area = (0, 0)
        self.state = Mouse.CLICK_STATE


    def end_hold(self):
        start_pos = (
            min(self.start_selcet_area[0], pg.mouse.get_pos()[0]),
            min(self.start_selcet_area[1], pg.mouse.get_pos()[1]))
        end_pos = (
            max(self.start_selcet_area[0], pg.mouse.get_pos()[0]),
            max(self.start_selcet_area[1], pg.mouse.get_pos()[1]))
        self.start_selcet_area = (start_pos[0] - cam_values.x, start_pos[1] - cam_values.y)
        self.end_selcet_area = (end_pos[0] - cam_values.x, end_pos[1] - cam_values.y)

        """
        self.agent_to_activate = activate_sprites_func(start_pos, end_pos)
        self.start_selcet_area = 0
        """

    """
    def ui_drag_effect(self, reactor, img, size, *args, **kwargs):
        return
    # self.create_cursor_image(UI_Image(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], size[0], size[1], img))
    # reactor.add_event_function(*args, **kwargs)
    # self.drag = True
    """
