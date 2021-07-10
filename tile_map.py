import pygame as pg
from settings import *
import numpy as np
from scipy.ndimage.interpolation import zoom



NUMBER_OF_CHUNKS_DEFUALT=50

class _Background_Sprite:
    def __init__(self,x, y, color, x_size, y_size):
        self.image = pg.Surface((x_size, y_size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.current_x = x
        self.current_y = y
        self.rect.x = x
        self.rect.y = y

class _Chunk:
    CHUNK_ON_SCREEN = -1

    def __init__(self, width, height, x, y):
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_x = x
        self.current_y = y
        self.tile_size_when_off_screen = _Chunk.CHUNK_ON_SCREEN  # in which tile_size did the chunk diisapeer

    def __str__(self):
        return f"size is {self.image.get_size()} and the position is {self.rect}"


class Map:
    """Map is basiccly some chunks with sprites on them according to a map file"""
    FOREST_BLOCK = '*'
    GROUND_BLOCK = '!'
    WATER_BLOCK = '.'

    def __init__(self, filename, number_of_chunks=NUMBER_OF_CHUNKS_DEFUALT, gen_new_map=False):
        self.data = []  # Consist of information about how to build the map (contains '.'/'1' in lines)

        if gen_new_map:
            self._gen_map(filename)

        with open(filename, 'rt') as map_data:
            for line in map_data:
                self.data.append(line.strip())

        self._number_of_chunks = number_of_chunks

        self.map_data = None  # change this later
        self.tile_map_data = None  # change this later




    def change_map(self,x_build_pos,y_build_pos,obj_size,type):
        """Change the map when building new object (changing tile_map map)"""
        #for load and save change this to more symbloes instead of just '*'
        temp_list = list(self.tile_map_data)
        for y in range(int(obj_size[1] / TILE_SIZE)+1):
            for x in range(int(obj_size[0]/TILE_SIZE)+1):
                """All objects are built from top left to bottom right, so we need to only check right and bottom"""
                index = (y+y_build_pos) * (int(MAP_WIDTH / TILE_SIZE)) + (x+x_build_pos)
                if index < len(temp_list):
                    temp_list[(y+y_build_pos) * (int(MAP_WIDTH / TILE_SIZE)) + (x+x_build_pos)] = type

        self.tile_map_data = ''.join(temp_list)



    def get_chunk_by_position(self,chunks,x_pos,y_pos):
        #returns chunk which the pos (x_pos and y_pos) fits in
        y_pos = int(y_pos / int(MAP_HEIGHT / self._number_of_chunks ))
        x_pos = int(x_pos / int(MAP_WIDTH / self._number_of_chunks ))

        chunk_index = y_pos * self._number_of_chunks + x_pos
        if 0 <= chunk_index < self._number_of_chunks**2:
            return chunks[chunk_index]
        return None

    def _create_chunks(self):
        """create chunks for map. chunks are large sprites where you can blit other sprites inside them."""
        chunks = []
        for y in range(self._number_of_chunks):
            for x in range(self._number_of_chunks):
                chunk = _Chunk(int(MAP_WIDTH / self._number_of_chunks), int(MAP_HEIGHT / self._number_of_chunks*1)
                              , x * MAP_WIDTH / self._number_of_chunks, y * MAP_HEIGHT / self._number_of_chunks * 1)

                chunks.append(chunk)

        return chunks

    def sqeeze_map(self,map_path,sqeeze_volume):
        #sqeeze the map to smaller map with the same properties


        #change this
        new_map = ""
        bad = 0
        with open(map_path, "r") as f:
            f = f.read()

            for y in range(0, int(MAP_HEIGHT / sqeeze_volume)):
                for x in range(0, int(MAP_WIDTH / sqeeze_volume)):
                    for i in range(sqeeze_volume):
                        for d in range(sqeeze_volume):
                            block_type = f[i * (MAP_WIDTH+1) + (y * sqeeze_volume * (MAP_WIDTH+1)) + (d + (x * sqeeze_volume))]
                            if block_type == ".":
                                bad = 1
                    if bad == 0:
                        new_map += "1"
                    else:
                        new_map += "."
                    bad = 0
        return new_map



    def load_map(self):
        """draw sprites on each chunk and returns all the updated chunks (chunks with sprites)"""
        chunks = self._create_chunks()
        for chunk in chunks:
            chunk.image.fill(GREEN)

            for y in range(int(chunk.rect.y),
                           int(chunk.rect.y ) + int(chunk.image.get_size()[1] )):
                for x in range(int(chunk.rect.x ),
                               int(chunk.rect.x ) + int(chunk.image.get_size()[0] )):
                    if self.data[y][x] == Map.FOREST_BLOCK:
                        s = _Background_Sprite(x - chunk.rect.x ,
                                               y - chunk.rect.y ,
                                               DARK_GREEN, 1, 1)
                        chunk.image.blit(s.image, s.rect)
                    elif self.data[y][x] == Map.GROUND_BLOCK:
                        s = _Background_Sprite(x - chunk.rect.x ,
                                               y - chunk.rect.y,
                                               BROWN, 1, 1)
                        chunk.image.blit(s.image, s.rect)
                    elif self.data[y][x] == Map.WATER_BLOCK:
                        s = _Background_Sprite((x - chunk.rect.x ), (y - chunk.rect.y ),
                             BLUE, 1, 1)
                        chunk.image.blit(s.image, s.rect)

        self.map_data = self.sqeeze_map(MAP_NAME, 1)  # change this later
        self.tile_map_data = self.sqeeze_map(MAP_NAME, TILE_SIZE)  # change this latersprite_manager
        return chunks


    @staticmethod
    def _gen_map(file_name):
        """simple map generator - writes to a file"""
        np.set_printoptions(threshold=10)

        raw_arr = np.random.uniform(size=(int(MAP_HEIGHT / 10), int(MAP_WIDTH / 10)))
        arr_of_numbers = zoom(raw_arr, 80)

        map_arr= []

        for arr in arr_of_numbers:
            row = []
            for i in arr:
                if i > 0.8:
                    row.append('.')
                elif i > 0.6:
                    row.append('*')
                elif i<0.15:
                    row.append('!')
                else:
                    row.append('1')
            map_arr.append(row)



        with open(file_name, "w") as f:
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    f.write(map_arr[y][x])
                f.write('\n')

    def update_map(self):
        pass
