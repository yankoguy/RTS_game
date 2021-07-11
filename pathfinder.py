import time
from heapq import heapify, heappush, heappop
from settings import TILE_SIZE,MAP_WIDTH,MAP_HEIGHT
import numpy
class Block:
    def __init__(self, x, y, step_value, value, previously, path_size=0):
        self.pos = (x, y)  # x is [0] y is [1]
        self.step_value = step_value
        self.value = value - path_size *0
        self.previously = previously
        self.path_size = path_size

    def __str__(self):
        # return f"vector : {self.pos}, value : {self.value}"
        return "vector : {self.pos}, value : {self.value}"

    def __lt__(self, other):
        return self.value < other.value


class PathFinder:
    def __init__(self):
        self.incomplete_paths = []


def get_distance(self_pos, target_pos):
    x_dis = abs(target_pos[0] - self_pos[0])
    y_dis = abs(target_pos[1] - self_pos[1])

    ##faster than max
    if x_dis > y_dis:
        bigger_axis = x_dis
        smaller_axis = y_dis
    else:
        bigger_axis = y_dis
        smaller_axis = x_dis

    return smaller_axis * 14 + (bigger_axis - smaller_axis) * 10


def dis_to_next_block(entity_pos, next_block_pos):
    if abs(entity_pos[0] - next_block_pos[0]) == abs(entity_pos[1] - next_block_pos[1]):
        return 14
    return 10


def get_neighbordes(entity, target, counter, map):
    neighbords = []

    for x in range(entity.pos[0] - 1, entity.pos[0] + 2):
        for y in range(entity.pos[1] - 1, entity.pos[1] + 2):
            if x >= 0 and y >= 0 and (entity.pos[0] != x or entity.pos[1] != y) and x<MAP_WIDTH/TILE_SIZE and y<MAP_HEIGHT/TILE_SIZE:
                if map[y*(int(MAP_WIDTH/TILE_SIZE))+x] != ".":
                    dis_to_next = dis_to_next_block(entity.pos, (x, y))

                    neighbords.append(Block(x, y, counter + dis_to_next,
                                            counter + dis_to_next + get_distance((x, y), target), entity,
                                            entity.path_size + 1))

    return neighbords


def search_in_incomple_paths(loop_counter, entity, incomple_paths):
    path = []
    STOP_CHECKING = 600  # if you didnt found after this number of iteration stop searching
    ADDING_PATH_BORDER = 400  # if there are less iteration than this number dont add this path
    if loop_counter < STOP_CHECKING:
        for incomple_path in incomple_paths:
            for pos in incomple_path:
                if pos == entity.pos:
                    # if found current pos find index of the pos in the list
                    index = incomple_path.index(pos)
                   # print("found", "path_index: ", incomple_paths.index(incomple_path), "place index: ", index)

                    # start filling the path with the blocks you already walked
                    while entity.previously is not None:
                        entity = entity.previously
                        path.insert(0, entity.pos)

                    # add the incomple to the path
                    for i in range(index + 1, len(incomple_path) - 1):
                        path.append(incomple_path[i])

                    # add it if lower than border
                    if loop_counter > ADDING_PATH_BORDER:
                        incomple_paths.insert(0, path)

                    return path
    return None

def fill_space_between_chunks(path,current_pos,next_pos): #because of the tiles the agent skips some pixels in his move so we fill them and that smooth the movment
    x,y = tuple(numpy.subtract(next_pos , current_pos))

    if x>0:
        x_val = 1
    else:
        x_val = -1

    if y>0:
        y_val=1
    else:
        y_val = -1

    for i in range(TILE_SIZE-1):
        if x != 0 and y !=0:
            path.insert(0,(current_pos[0]+(1+i)*x_val,current_pos[1]+(i+1)*y_val))
        elif x == 0: #need to only change y
            path.insert(0,(current_pos[0],current_pos[1]+(i+1)*y_val))

        else: #need to only change x:
            path.insert(0,(current_pos[0]+(i+1)*x_val,current_pos[1]))

def a_star(map, entity, target, all_paths=None,time_to_stop = 0.5):
    if all_paths is None:
        all_paths = []

    start_time = time.time()
    known_neighbers = []
    heapify(known_neighbers)
    open_set = set()
    loop_counter = 0  # how many runs it took to finish finding the path

    entity.pos = (int(entity.pos[0] /TILE_SIZE) , int(entity.pos[1]/TILE_SIZE))

    #print(
     #   f'self point : {entity.pos} target point : {target}, known_n_number : {len(known_neighbers)}')
    target = (target[0] / TILE_SIZE,target[1]/TILE_SIZE)
    while True:
        if time.time()-start_time > time_to_stop:
            print("stopped")
            return None
        if entity.pos == (round(target[0]),round(target[1])): #round because the distance can be smaller than the Tile size
            path = [(target[0] * TILE_SIZE,target[1]*TILE_SIZE)]
            while entity.previously is not None:
                fill_space_between_chunks(path,(entity.pos[0] *TILE_SIZE , entity.pos[1] * TILE_SIZE),(entity.previously.pos[0] *TILE_SIZE , entity.previously.pos[1] * TILE_SIZE))

                entity = entity.previously
                path.insert(0, (entity.pos[0] *TILE_SIZE , entity.pos[1] * TILE_SIZE))

            all_paths.insert(0, path)

            return path.copy()

       # path = search_in_incomple_paths(loop_counter, entity, all_paths)
       # if path is not None:
        #    print(len(path))
         #   return path.copy()

        neighbordes = get_neighbordes(entity, target, entity.step_value,
                                      map)  # get all neightboards from -1 to 1 pos

        for n in neighbordes:
            if n.pos not in open_set:
                open_set.add(n.pos)
                heappush(known_neighbers, n)  # add to the point list all the neighbords that are not blocked

        c_all = heappop(known_neighbers)  # get the closest of all neighbordes

        loop_counter += 1
        entity = c_all


if __name__ == '__main__':
    print(get_distance((0, 0), (122, 65456)))
