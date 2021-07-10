import pygame as pg
from settings import *


class Cam_values:
    def __init__(self):
        self.tile_size = 0
        self.x = 0
        self.y = 0

    def update_values(self, tile_size, x, y):
        self.tile_size = tile_size
        self.x = x
        self.y = y


cam_values = Cam_values()


class Camera:
    MINIMUN_TILE_SIZE = 1
    MAXIMUN_TILE_SIZE = 5

    def __init__(self, width, height, camera_speed, camera_scroll_speed, reactor):
        self.rect = pg.Rect(0, 0, width, height)
        self._width = width
        self._height = height
        self._camera_move_speed = camera_speed
        self._camera_scroll_speed = camera_scroll_speed
        self.tile_size = Camera.MINIMUN_TILE_SIZE
        self.updated = False
        self.add_funcion_to_reactor(reactor)

    def camera_scrolling_up(self):
        if self.tile_size < Camera.MAXIMUN_TILE_SIZE:
            self.tile_size += self._camera_scroll_speed
            self.updated = False

    def camera_scrolling_down(self):
        if self.tile_size > Camera.MINIMUN_TILE_SIZE:
            self.tile_size -= self._camera_scroll_speed
            self.updated = False

    def add_funcion_to_reactor(self, reactor):
        reactor.add_event_function(pg.MOUSEBUTTONDOWN, 4, "button", self.camera_scrolling_up)
        reactor.add_event_function(pg.MOUSEBUTTONDOWN, 5, "button", self.camera_scrolling_down)

        # reactor.add_key_function(pg.K_a,lambda  : print("a"))

    def apply_scale(self, image):

        return pg.transform.scale(image, (
            int(image.get_size()[0] * self.tile_size),
            int(image.get_size()[1] * self.tile_size)))

    def apply_pos(self, entity):
        entity.rect.x = entity.current_x * self.tile_size
        entity.rect.y = entity.current_y * self.tile_size

        return entity.rect.move(self.rect.topleft)

    def camera_movment_check(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        WINDOW = 50  # how much the play can exeed from the map
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.rect.x * self.tile_size < SCREEN_WIDTH * self.tile_size:
            self.vx -= self._camera_move_speed
            # self.updated = False

        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.rect.x > -MAP_WIDTH * self.tile_size:
            self.vx = self._camera_move_speed
            # self.updated = False

        if (keys[pg.K_UP] or keys[pg.K_w]) and self.rect.y * self.tile_size < SCREEN_HEIGHT * self.tile_size:
            self.vy -= self._camera_move_speed
        # self.updated = False

        if (keys[pg.K_DOWN] or keys[pg.K_s]) and self.rect.y > -MAP_HEIGHT * self.tile_size:
            self.vy = self._camera_move_speed
        #   self.updated = False

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def camera_movment(self, delta_time):
        # change this with the reactor
        self.camera_movment_check()
        self.rect.x -= self.vx * delta_time
        self.rect.y -= self.vy * delta_time

    def camera_update(self, delta_time):
        self.camera_movment(delta_time)
        cam_values.update_values(self.tile_size, self.rect.x, self.rect.y)
