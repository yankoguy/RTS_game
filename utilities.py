import math

def on_object(pos, upper_point, lower_point):
    if upper_point[0] <= pos[0] <= lower_point[0] and upper_point[1] <= pos[1] <= lower_point[1]:
        return True
    return False



