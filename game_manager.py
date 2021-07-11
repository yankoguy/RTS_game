import pygame as pg
from settings import *
from event_manager import Reactor
from settings import OPENING_SCENE
from grafics import GameWorld
from Mouse_manager import Mouse
from Render_system import Renderer



class _Clock:
    """consits all the information about time: delta_time, game timer, time in which time the was last played """

    def __init__(self):
        self._clock = pg.time.Clock()
        self.delta_time = 0
        self.game_timer = 0
        self._last_play = 0  # time from last save

    def clock_update(self):
        self.delta_time = self._clock.tick(FPS) / 1000
        self.game_timer += self.delta_time

class Manager:
    """ This is the class that controls everything in the game"""

    def __init__(self):
        self.reactor =None
        self._game_clock = None
        self._playing = True
        self.my_mouse = None
        self.grafics_manager = None
        self.renderer = None

        self._stopped = True
        self.state = OPENING_SCENE
        pg.init()
        pg.font.init()


        self.awake()
        self.start()
        self.game_loop()

    def awake(self):
        """create all objects without dependence(before start)"""
        pg.display.set_caption(TITLE)
        self._game_clock = _Clock()

        self.my_mouse = Mouse()
        self.reactor = Reactor(self.my_mouse.mouse_event_handler)
        self.renderer = Renderer(self.reactor,WHITE)

        self.grafics_manager = GameWorld(self.reactor)


    def start(self):
        """create all objects with dependence"""
        self.grafics_manager.sprite_manager.start()


    def game_loop(self):
        """the loop"""
        while self._playing:
            self.events()

            if not self.grafics_manager.UI_manager.in_scene:
                self.update()
            else: #in ui scene
                self.renderer.fill_screen(WHITE)
                self.renderer.render_objects(self.grafics_manager.UI_manager.current_scene,1)
                pg.display.update()

                #self.grafics_manager.draw_stop_game_ui()


    def render(self):
        self.renderer.draw_background(self.grafics_manager.background)
        self.renderer.render_objects(self.grafics_manager.sprite_manager.all_sprites)
        self.renderer.render_objects(self.grafics_manager.UI_manager.current_scene,1)
        self.renderer.render_objects(self.grafics_manager.UI_manager.get_shown_menus(),1)
        self.renderer.render_objects([self.grafics_manager.UI_manager.cursor],2)

        self.renderer.draw_square(self.my_mouse.start_selcet_area,self.my_mouse.end_selcet_area)
        pg.display.update()

    def events(self):
        self.reactor.activate_functions()
#        self.reactor.activate_keys_function()


    def update(self):
        self._game_clock.clock_update()
        self.render()

        self.renderer.camera.camera_update(self._game_clock.delta_time)
        self.grafics_manager.sprite_manager.update_sprites(self._game_clock.delta_time)
        self.grafics_manager.UI_manager.cursor.update()
        self.my_mouse.update()

      #  self.grafics_manager.draw_lines()
        #print(self._game_clock._clock.get_fps())
        pg.display.update()


if __name__ == '__main__':
    m = Manager()
