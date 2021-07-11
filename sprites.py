import pygame as pg
from settings import *
import threading
import pathfinder
import utilities
import random
from tile_map import Map
from camera import cam_values

from Mouse_manager import Mouse

GATHERHOUSE = 0
GATHER_MAN = 1
ARMYHOUSE = 2
SOLIDER = 3


TREE_TYPE = 1
STONE_TYPE = 2




class Sprite_manager:
    def __init__(self, map, reactor,get_nearest_tile):
        self.walls = None
        self.all_sprites = None
        self.agents = []
        self.clickable_sprites = []
        self.sprites_paths = []
        self.squuzed_map = map

        self.selected_agents = []

        self.alive_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()


            #reactor.add_mouse_event(pg.MOUSEBUTTONUP, 1, "button", self.get_agents_in_area,Mouse.CLICK_STATE)

        reactor.add_event_function(pg.MOUSEBUTTONDOWN, 1, "button", self.sprite_click)
        reactor.add_mouse_event(pg.MOUSEBUTTONUP, 1, "button", self.select_agents)
        reactor.add_mouse_event(pg.MOUSEBUTTONDOWN, 1, "button", self.active_agents,get_nearest_tile)

    def add_resources(self,map):
        chance = 3000
        for y,line in enumerate(map.data[:-20]):
            for x,block in enumerate(line):
                if block == Map.FOREST_BLOCK:
                    if random.randint(1,chance) == 5:
                        self.create_Tree(x,y)
                        map.change_map(round(x/TILE_SIZE),round(y/TILE_SIZE),TREE_SIZE, '4')

                if block == Map.GROUND_BLOCK:
                    if random.randint(1, chance) == 5:
                        self.create_Stone(x, y)
                        map.change_map(round(x/TILE_SIZE),round(y/TILE_SIZE), STONE_SIZE,'5')

    def sprite_click(self):
        for clickable_sprite in self.clickable_sprites:
            if utilities.on_object(((pg.mouse.get_pos()[0] - cam_values.x) / cam_values.tile_size, (pg.mouse.get_pos()[1] - cam_values.y) / cam_values.tile_size),
                                    (clickable_sprite.rect.x / cam_values.tile_size,clickable_sprite.rect.y / cam_values.tile_size),
                                    (clickable_sprite.rect.x / cam_values.tile_size + clickable_sprite.image.get_width() ,(clickable_sprite.rect.y / cam_values.tile_size + clickable_sprite.image.get_height()))):
                # check what type of clickable it is
                clickable_sprite.on_click()
                break

    def start(self):
        self.inillizing_first_sprites()

    def create_ArmyHouse(self,create_ui_menu, x, y):
        army_house = _ArmyHouse(self.all_sprites, x, y, ARMY_HOUSE_SIZE[0], ARMY_HOUSE_SIZE[1], ARMYHOUSE, self.create_army_man ,create_ui_menu, "tower2.png")
        self.clickable_sprites.append(army_house)
        return army_house

    def create_GatherHouse(self,create_ui_menu,x,y):
        gather_house = _GatherHouse(self.all_sprites, x, y, GATHER_HOUSE_SIZE[0],GATHER_HOUSE_SIZE[1], GATHERHOUSE, self.create_gather_man, create_ui_menu,"tower.jpg")
        self.clickable_sprites.append(gather_house)
        return gather_house

    def create_Tree(self, x, y):
        tree = _Tree(self.all_sprites, x, y, TREE_SIZE[0], TREE_SIZE[1], TREE_TYPE, 30, "tree.png")
        #self.all_sprites.add(tree)
        return tree

    def create_Stone(self, x, y):
        stone = _Stone(self.all_sprites, x, y, STONE_SIZE[0], STONE_SIZE[1], STONE_TYPE, 25, "stone.png")
        #self.all_sprites.add(stone)
        return stone

    def create_gather_man(self,x,y):
        gather_man = _Gather_man([self.all_sprites,self.alive_sprites], x + random.randint(0, GATHER_HOUSE_SIZE[0] / 2),y
                    , 8, 8, GATHER_MAN, image_name="gather_man.png")

        self.agents.append(gather_man)
        self.clickable_sprites.append(gather_man)


    def create_army_man(self):
        pass


    def inillizing_first_sprites(self):
        # create first sprites
        pass
        # self.clickable_sprites.append(GatherHouse(self.all_sprites, 0,0, 20000, 20000,GATHERHOUSE,self.all_sprites,"tower.jpg"))

        # self.clickable_sprites.append(GatherHouse(self.all_sprites, 400, 500, BLACK, 100, 100,GATHERHOUSE,self.all_sprites))

    def update_sprites(self, delta_time):
        self.alive_sprites.update(delta_time)


    def get_agents_in_area(self,start_pos,end_pos):
        agents_in_area = []
        for agent in self.agents:
            if utilities.on_object((agent.rect.x, agent.rect.y), start_pos, end_pos):
                agents_in_area.append(agent)
        return agents_in_area

    def select_agents(self,start_pos,end_pos):
        self.selected_agents = self.get_agents_in_area(start_pos,end_pos)



    def active_agents(self,target_x,target_y,get_nearest_tile):
        # change this once i have more groups
        for agent in self.selected_agents:
            x = target_x / cam_values.tile_size - cam_values.x / cam_values.tile_size
            y = target_y / cam_values.tile_size - cam_values.y / cam_values.tile_size
            new_x,new_y,surface = get_nearest_tile((x,y),WATER)
            #if surface is not None:
            agent.start_pathfinding(self.squuzed_map, self.sprites_paths,(new_x,new_y),surface)
        self.selected_agents=[]

class BasicObject(pg.sprite.Sprite):
    def __init__(self, groups, x, y, x_size, y_size, object_type, image_name=None, bg_color = None):
        if groups is not None:
            pg.sprite.Sprite.__init__(self, groups)
        if image_name is not None:
            self.image = pg.image.load(image_name).convert_alpha()
            self.image = pg.transform.scale(self.image, (x_size, y_size))
        else:
            self.image = pg.Surface((x_size, y_size))
            self.image.fill(bg_color)

        self.rect = self.image.get_rect()
        self.current_x = x
        self.current_y = y
        self.rect.x = x
        self.rect.y = y
        self.sprite_type = object_type



class __Sprite(BasicObject):

    # the size and color will be replace with an image

    def __init__(self, groups, x, y, x_size, y_size, object_type, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, image_name)
        self.updated = 0
        self._timer = 0


class __StaticSprite(__Sprite):
    def __init__(self, groups, x, y, x_size, y_size, object_type, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, image_name)


class __Resource(__StaticSprite):
    def __init__(self, groups, x, y, x_size, y_size, object_type, quantity, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, image_name)
        self.quantity = quantity

    def get_resource(self,amount):
        self.quantity-=amount
        return amount

    def disappear(self):
        pass


class _Tree(__Resource):
    def __init__(self, groups, x, y, x_size, y_size, object_type, quantity, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, quantity, image_name)
        self.quantity = quantity


class _Stone(__Resource):
    def __init__(self, groups, x, y, x_size, y_size, object_type, quantity, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, quantity, image_name)
        self.quantity = quantity




class __ClickAbleSprite(__Sprite):
    def __init__(self, groups, x, y, x_size, y_size, object_type, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, image_name)

    def on_click(self):
        pass





class __AliveSprite(__ClickAbleSprite):
    def __init__(self, group, x, y, x_size, y_size, object_type, image_name=None):
        super().__init__(group, x, y, x_size, y_size, object_type, image_name)

        self.speed = 100

    # should threaded

    def move(self):
        pass

    def update(self, delta_time):
        if delta_time < 0.2:  # if there was a lag for more than a sec ignore this time
            self._timer += delta_time
        self.move()


class __Agent(__AliveSprite):
    def __init__(self, group, x, y, x_size, y_size, object_type,image_name=None):
        super().__init__(group, x, y, x_size, y_size, object_type, image_name)
        self.target_x = -1
        self.target_y = -1
        self.target_type ='' #what object is the agent is about to go to
        self.path = []
        self.x_random = random.randint(-5,5)
        self.y_random = random.randint(-5,5)

        self.block = None

    def start_pathfinding(self, map, sprites_paths,target_pos,target_type):
        self.block = pathfinder.Block(int(self.current_x), int(self.current_y), 0, 0, None)
        self.target_x,self.target_y = target_pos
        self.target_type = target_type
        self._timer = 0  # reset the timer in order to prevent big jumps at the start of the movment (because it a* pause the game for a few moment so the timer will grow and a big movment in agent will occur)
        t =  threading.Thread(target=self.pathfinding,args=(map,self.target_x,self.target_y,sprites_paths.copy()))
        t.start()

    def pathfinding(self,map,x_pos,y_pos,sprites_paths):
        self.path = pathfinder.a_star(map, self.block, (x_pos, y_pos), all_paths=sprites_paths.copy())

    def move(self):
        count = 0
        while self._timer > (1 / self.speed):
            if self.path is not None and self.path != []:
                count+=1
                point_in_path = self.path.pop(0)
                x, y = point_in_path
                self.current_x = x + self.x_random
                self.current_y = y + self.y_random

            self._timer -= 1 / self.speed


class __Creators(__ClickAbleSprite):
    def __init__(self, groups, x, y, x_size, y_size, object_type, creation_function,image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, image_name)
        self.creation_function = creation_function

    def create_obj(self):
        self.creation_function()

class _GatherHouse(__Creators):
    def __init__(self, groups, x, y, x_size, y_size, object_type, creation_function,create_ui_menu, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, creation_function,image_name)
        #self.menu = create_ui_menu(x+self.image.get_size()[0],y)
        #self.menu.add_button(WHITE,100,50,"gather man",BLACK,self.create_man)

    def on_click(self):

        """
        if self.menu.show:
            self.menu.show = False
        else:
            self.menu.show = True
        """
        self.create_obj()

    def create_obj(self):
        self.creation_function(self.current_x + random.randint(0, GATHER_HOUSE_SIZE[0] / 2),
                    self.current_y + GATHER_HOUSE_SIZE[1])

class _ArmyHouse(__ClickAbleSprite):
    def __init__(self, groups, x, y, x_size, y_size, object_type,creation_function, create_ui_menu, image_name=None):
        super().__init__(groups, x, y, x_size, y_size, object_type, creation_function,image_name)
     #   create_ui_menu(x,y)

    def on_click(self):
        # create solider
        _Solider(self.groups, self.current_x + random.randint(0, ARMY_HOUSE_SIZE[0] / 2),
                                            self.current_y + ARMY_HOUSE_SIZE[1]
                                            , YELLOW, 8, 8, SOLIDER, 4, 5)


class _Gather_man(__Agent):
    def __init__(self, group, x, y, x_size, y_size, object_type, image_name=None):
        super().__init__(group, x, y, x_size, y_size, object_type,image_name)
        self.target_y += GATHER_HOUSE_SIZE[1]

    def action(self):
        print("action")

class _Solider(__Agent):
    def __init__(self, group, x, y, x_size, y_size, object_type, power, defence, image_name=None):
        super().__init__(group, x, y, x_size, y_size, object_type, image_name)
        self.power = power
        self.defence = defence


