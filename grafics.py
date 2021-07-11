import pygame as pg
from settings import *
from os import path
from camera import Camera
from tile_map import Map
import utilities
from sprites import Sprite_manager, BasicObject
from camera import cam_values
from Mouse_manager import Mouse

BOUTTON = 10

SOME_RANDOM_VALUE = 101

class GameWorld:
    """Controls UI , sprites, map and mouse (maybe i will change the mouse). His job is to draw everything to the screen"""


    def __init__(self, reactor):
        self._map = None
        self.background = None
        self.sprite_manager = None
        self.UI_manager = None
        self.load_data()

        self.sprite_manager = Sprite_manager(self._map.tile_map_data, reactor,
                                             self._map.get_nearest_tile)

        self.sprite_manager.add_resources(self._map)

        self.UI_manager = UI_manager(reactor, self.create_building_sprite)

        # reactor.add_mouse_event(pg.MOUSEBUTTONDOWN, 1, "button", self.get_type_of_surface,Mouse.CLICK_STATE,pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])
        # reactor.add_event_function(pg.MOUSEBUTTONDOWN, 1, "button", self.get_type_of_surface,pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])


    def create_building_sprite(self, ui_menu_func, building_number=1):
        """create a static sprite on the map"""
        x = int((pg.mouse.get_pos()[0] - cam_values.x) / (cam_values.tile_size * TILE_SIZE))
        y = int((pg.mouse.get_pos()[1] - cam_values.y) / (cam_values.tile_size * TILE_SIZE))

        if building_number == 1:
            if self._can_build(x, y, GATHER_HOUSE_SIZE):
                self.sprite_manager.create_GatherHouse(ui_menu_func, round(x) * TILE_SIZE, round(y) * TILE_SIZE)
                self._map.change_map(x, y, GATHER_HOUSE_SIZE, '?')
        elif building_number == 2:
            if self._can_build(x, y, ARMY_HOUSE_SIZE):
                self.sprite_manager.create_ArmyHouse(ui_menu_func, round(x) * TILE_SIZE, round(y) * TILE_SIZE)
                self._map.change_map(x, y, ARMY_HOUSE_SIZE, '?')


    def _can_build(self, x_build_pos, y_build_pos, obj_size):
        """Check if building can build and will not be built on something else"""
        for y in range(int(obj_size[1] / TILE_SIZE) + 1):
            for x in range(int(obj_size[0] / TILE_SIZE) + 1):
                if self.get_type_of_surface((x + x_build_pos), (y + y_build_pos)) != GROUND:
                    return False
        return True

    def get_type_of_surface(self, x, y):
        """get the type of the surface the mouse is currently on"""
        # it wont work well if the map size isn't like the map.txt file size (width and height)
        if x < 0 or x > MAP_WIDTH or y < 0 or y > MAP_HEIGHT:
            return OUT
        mouse_type = self._map.tile_map_data[y * (int(MAP_WIDTH / TILE_SIZE)) + x]
        if mouse_type == '.':
            return WATER
        elif mouse_type == '?':  # change this to on sprite
            return OBJECT
        elif mouse_type == '4':
            return TREE
        elif mouse_type == '5':
            return STONE
        elif self.UI_manager.get_ui() is not None:
            return UI
        return GROUND


    def load_data(self):
        """Load map data"""
        game_folder = path.dirname(__file__)
        self._map = Map(path.join(game_folder, 'map.txt'), gen_new_map=False)
        self.background = self._map.load_map()


class UI_manager:
    def __init__(self, reactor, create_building_func):
        self.font = pg.font.SysFont('Comic Sans MS', 20)

        self.current_scene = None
        self.canvases = []
        self.menus = []
        self.in_scene = True

        self.canvases.insert(OPENING_SCENE, pg.sprite.Group())
        self.canvases.insert(IN_GAME_SCENE, pg.sprite.Group())

        self.create_first_canvas()
        self.create_in_game_canvas()


        self.cursor = Cursor(None, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 8, 8,
                             SOME_RANDOM_VALUE, reactor,"tree.png")


        #   self.create_menu()

        self.create_GatherHouse_ui(reactor, create_building_func,self.cursor.change_cursor_image)

        self.current_scene = self.canvases[OPENING_SCENE]
        reactor.add_event_function(pg.MOUSEBUTTONDOWN, 1, "button", self.ui_click)


    def get_shown_menus(self):
        menu_entities = []
        for menu in self.menus:
            if menu.show and self.canvases[menu.scene] == self.current_scene:
                for entity in menu.entities:
                    menu_entities.append(entity)
        return menu_entities

    def ui_click(self):
        ui_entity = self.get_ui()
        if ui_entity is not None:
            ui_entity.on_click()

    def get_ui(self):
        # change this function
        for ui_entity in self.current_scene:
            if utilities.on_object((pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]),
                                   (ui_entity.rect.x, ui_entity.rect.y),
                                   (ui_entity.rect.x + ui_entity.image.get_width(),
                                    ui_entity.rect.y + ui_entity.image.get_height())):
                return ui_entity

        for ui_entity in self.get_shown_menus():
            if utilities.on_object(((pg.mouse.get_pos()[0] - cam_values.x) / cam_values.tile_size,
                                    (pg.mouse.get_pos()[1] - cam_values.y) / cam_values.tile_size),
                                   (ui_entity.rect.x / cam_values.tile_size,
                                    ui_entity.rect.y / cam_values.tile_size),
                                   (ui_entity.rect.x / cam_values.tile_size + ui_entity.image.get_width(), (
                                           ui_entity.rect.y / cam_values.tile_size + ui_entity.image.get_height()))):
                return ui_entity

        return None

    def create_in_game_canvas(self):
        _Button(self.canvases[IN_GAME_SCENE], 800, 0, LIGHTGREY, 200, 50, self.font, "in game", WHITE,
                lambda: print("x"))
        _Button(self.canvases[IN_GAME_SCENE], 0, 500, LIGHTGREY, 100, 50, self.font, "Menu", WHITE,
                lambda: self.replace_scene(MENU_SCENE))

    def create_clickableobject_menu_ui(self, x, y):
        pass
        """
        menu = _UI_menu(x, y, self.font, IN_GAME_SCENE)
        self.menus.append(menu)
        #    self.canvases[IN_GAME_SCENE].ui_entites.append(menu)
        return menu
        """

    def create_first_canvas(self):
        _Button(self.canvases[OPENING_SCENE], 500, 300, LIGHTGREY, 200, 50, self.font, "Play", WHITE,
                lambda: self.replace_scene(IN_GAME_SCENE))
        _Button(self.canvases[OPENING_SCENE], 250, 300, LIGHTGREY, 200, 50, self.font, "Quit", WHITE,
                lambda: print("quit"))

    """
    def create_menu(self):
        menu_scene = _Canvas(MENU_SCENE)
        menu_scene.ui_entites.append(_Button(500,300,LIGHTGREY,500,50,self.font,"Welocme To settings",WHITE, lambda : print("settings")))
        menu_scene.ui_entites.append(_Button(250,300,LIGHTGREY,200,100,self.font,"Return",WHITE, lambda : self.replace_scene(IN_GAME_SCENE)))

        self.canvases.insert(menu_scene.canvas_id,menu_scene)
    """

    def create_GatherHouse_ui(self, reactor, create_GatherHouse_func,change_cursor_func):
        # the create function is the function in the grafic manager

        _Button(self.canvases[IN_GAME_SCENE], 250, 600, LIGHTGREY, 300, 100, self.font, "Build GatherHouse", WHITE,
                [lambda : change_cursor_func("tower.jpg",GATHER_HOUSE_SIZE[0],GATHER_HOUSE_SIZE[1]),
                 lambda: reactor.add_event_function(pg.MOUSEBUTTONDOWN, 1, "button", create_GatherHouse_func,None,1,one_time=True)])


    def replace_scene(self, state=0):
        self.current_scene = self.canvases[state]

        if state != IN_GAME_SCENE:
            self.in_scene = True
        else:
            self.in_scene = False


class Cursor(BasicObject):
    def __init__(self, groups, x, y, x_size, y_size, object_type, reactor,image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, image_name)
        reactor.add_event_function(pg.MOUSEBUTTONDOWN, 1, "button",self.clear_image)

    def update(self):
        self.rect.x = pg.mouse.get_pos()[0]
        self.rect.y = pg.mouse.get_pos()[1]

    def change_cursor_image(self,new_image,x_size,y_size):
        self.image = pg.image.load(new_image).convert_alpha()
        self.image = pg.transform.scale(self.image, (x_size, y_size))

    def clear_image(self):
        self.image.fill(NO_COLOR)



class _Button(BasicObject):
    def __init__(self, scene, x, y, bg_color, x_size, y_size, font, text, text_color, functions_to_activate):
        super().__init__(scene, x, y, x_size, y_size, BOUTTON, image_name=None, bg_color=bg_color)
        self.functions_to_activate = functions_to_activate

        self.text = font.render(text, 1, text_color)
        self.image.blit(self.text, (0, 0))

        if type(functions_to_activate) != list:
            #if only one function was passed change it to list
            self.functions_to_activate = [functions_to_activate]

    def on_click(self):
        for func in self.functions_to_activate:
            func()


"""
class _UI_menu:
    def __init__(self, x, y, font, scene):
        self.pos = (x, y)
        self.scene = scene
        self.font = font
        self.entities = []
        self.header = ""
        self.all_buttons_height = 0
        self.show = False

    def add_button(self, bg_color, x_size, y_size, text, text_color, function_to_activate):
        self.entities.append(
            _Button(self.pos[0], self.pos[1] + self.all_buttons_height, bg_color, x_size, y_size, self.font, text,
                    text_color, function_to_activate))
        self.all_buttons_height += y_size + 5
"""
