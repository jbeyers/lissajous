from simple_svg import Scene, Line
from IPython.display import SVG
import math
import serial
from ipywidgets import interact


@interact(multiplier=(1, 3), offset=(0.0, 0.03, 0.001), starter=(0.0, 3.142, 0.002), circle_size=(0.0, 1.0, 0.01), circle_speed=(0.0, 3.0, 1.0), circle_offset=(-0.05, 0.05, 0.001), circle_start=(0.0, 3.142, 0.002))
def harmonograph(multiplier, offset, starter, circle_size, circle_speed, circle_offset, circle_start):
    pos = 0
    spd = 0.05
    decay = 6000
    factor = multiplier + offset
    circle_factor = circle_speed + circle_offset
    min_x = max_x = min_y = max_y = prev_x = prev_y = 400
    points = []
    for pos in range(decay//10, decay):
        adjx = int(400 + int(200 * (pos/float(decay)) * math.sin(pos * spd)))
        adjy = int(400 + int(200 * (pos/float(decay)) * math.sin(starter + (pos * spd * factor))))
        adjx += int(circle_size * 200 * (pos/float(decay)) * math.sin(circle_start + (pos * spd * circle_factor)))
        adjy += int(circle_size * 200 * (pos/float(decay)) * math.cos(circle_start + (pos * spd * circle_factor)))
        points.append([adjx, adjy])
        min_x = min(min_x, adjx)
        min_y = min(min_y, adjy)
        max_x = max(max_x, adjx)
        max_y = max(max_y, adjy)

    scale = min(800.0/(max_x - min_x), 800.0/(max_y - min_y))
    x_offset = ((max_x + min_x)/2 - 400)*70/400
    y_offset = ((max_y + min_y)/2 - 400)*70/400

    ser = serial.Serial('/dev/ttyACM0', 9600)
    tosend = f'{factor} {starter} {circle_size} {circle_factor} {circle_start} {x_offset} {y_offset} {scale:.4f}'
    print(tosend)
    ser.write(tosend.encode('utf-8'))

    scene = Scene('test', 800, 800)
    for point in points:
        point_x = scale*(point[0] - min_x)
        point_y = scale*(point[1] - min_y)
        scene.add(Line((prev_x, prev_y), (point_x, point_y)))
        prev_x, prev_y = point_x, point_y

    return SVG("\n".join(scene.strarray()))
