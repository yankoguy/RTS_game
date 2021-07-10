from camera import Camera
from settings import *
import pygame as pg


class Renderer:
    def __init__(self, reactor, color):
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT, 500, 1, reactor)
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color_to_fill = color

    def fill_screen(self, color=None):
        if color is None:
            color = self.color_to_fill
        self._screen.fill(color)

    def render_objects(self, objects_to_render, mode=0):
        if mode == 0:
            for obj in objects_to_render:
                self._screen.blit(self.camera.apply_scale(obj.image), self.camera.apply_pos(obj))
        elif mode == 1:
            for obj in objects_to_render:
                self._screen.blit(obj.image, obj.rect)
        elif mode == 2:
            for obj in objects_to_render:
                self._screen.blit(self.camera.apply_scale(obj.image), obj.rect)

    def draw_square(self, start, end):
        pg.draw.rect(self._screen, WHITE, pg.Rect(start[0], start[1],
                                                  end[0] - start[0],
                                                  end[1] - start[1]), 2)

    def draw_lines(self):
        # drops the FPS from 66 - 55
        for x in range(0, SCREEN_WIDTH, TILE_SIZE * self.camera.tile_size):
            pg.draw.line(self._screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE * self.camera.tile_size):
            pg.draw.line(self._screen, BLACK, (0, y), (SCREEN_WIDTH, y))

    def draw_background(self, background):
        # Draw screen's background by chunks
        self._screen.fill(DARK_BLUE)
        renderd_chunks = 0  ###how many chunks have been rendered this frame

        for chunk in background:
            ###if chunk is in screen borders draw it
            if (
                    -chunk.image.get_size()[
                        0] * self.camera.tile_size < self.camera.rect.x + chunk.rect.x < SCREEN_WIDTH and
                    -chunk.image.get_size()[
                        1] * self.camera.tile_size < self.camera.rect.y + chunk.rect.y < SCREEN_HEIGHT):
                chunk.tile_size_when_off_screen = -1

                self._screen.blit(self.camera.apply_scale(chunk.image), self.camera.apply_pos(chunk))
                renderd_chunks += 1

            elif not self.camera.updated:  # should change it to update only the sprites that will be shown after changing the size of the camera (tile size) by compuiing the positions
                self._screen.blit(self.camera.apply_scale(chunk.image), self.camera.apply_pos(chunk))

        self.camera.updated = True

        # print(f"There are {len(self.background)} chunks, {renderd_chunks} are rendered this frame, which is { renderd_chunks / len(self.background) * 100} precenteges")

    """       
     def draw_sprites(self, delta_time):
        for sprite in self.sprite_manager.all_sprites:
            self._screen.blit(self.camera.apply_scale(sprite.image), self.camera.apply_pos(sprite))
                # if sprite.sprite_type != GATHERHOUSE:
            # update all sprites in group

            # pg.display.update()
    """

    """
    def draw_ui_menus(self):
        for ui_menu in self.UI_manager.get_shown_menus():
            self._screen.blit(self.camera.apply_scale(ui_menu.image), self.camera.apply_pos(ui_menu))
    """
    """
    def draw_ui(self):
        for ui_entite in self.UI_manager.current_scene.ui_entites:
            self._screen.blit(ui_entite.image, ui_entite.rect)
        self.draw_ui_menus()
    """

    """
    def draw_mouse_select_area(self):
        if self.mouse.select_mode:
            pg.draw.rect(self._screen, WHITE, pg.Rect(self.mouse.start_selcet_area[0], self.mouse.start_selcet_area[1],
                                                          pg.mouse.get_pos()[0] - self.mouse.start_selcet_area[0],
                                                          pg.mouse.get_pos()[1] - self.mouse.start_selcet_area[1]), 2)
    """

    """
    def draw_mouse_cursor(self):
        #Draw mouse sprite if it does exist
        if self.mouse.cursor is not None:
            self._screen.blit(self.mouse.cursor.image, self.mouse.cursor.rect)
    """
    """
    def draw_stop_game_ui(self):  # draw ui that stop the game (Like settings)
        #Draw a specific UI when the game is stopped
        self._screen.fill(YELLOW)
        self.draw_ui()
        pg.display.update()
    """

    """
    def draw_lines(self):
        # drops the FPS from 66 - 55
        for x in range(0, SCREEN_WIDTH, TILE_SIZE * self.camera.tile_size):
            pg.draw.line(self._screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE * self.camera.tile_size):
            pg.draw.line(self._screen, BLACK, (0, y), (SCREEN_WIDTH, y))
    """
    """
    def draw_background(self):
        #Draw screen's background by chunks
        self._screen.fill(DARK_BLUE)
        renderd_chunks = 0  ###how many chunks have been rendered this frame

        for chunk in self.background:
            ###if chunk is in screen borders draw it
            if (
                    -chunk.image.get_size()[
                        0] * self.camera.tile_size < self.camera.camera.x + chunk.rect.x < SCREEN_WIDTH and
                    -chunk.image.get_size()[
                        1] * self.camera.tile_size < self.camera.camera.y + chunk.rect.y < SCREEN_HEIGHT):
                chunk.tile_size_when_off_screen = -1

                self._screen.blit(self.camera.apply_scale(chunk.image), self.camera.apply_pos(chunk))
                renderd_chunks += 1

            elif not self.camera.updated:  # should change it to update only the sprites that will be shown after changing the size of the camera (tile size) by compuiing the positions
                self._screen.blit(self.camera.apply_scale(chunk.image), self.camera.apply_pos(chunk))

        self.camera.updated = True

            # print(f"There are {len(self.background)} chunks, {renderd_chunks} are rendered this frame, which is { renderd_chunks / len(self.background) * 100} precenteges")
    """
