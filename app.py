from flask import Flask, render_template, request, redirect
import svgwrite
from svgwrite.shapes import Polyline, Line
import math
import random
# from simplesvg import SVG


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

def harmonograph(ratio, starter, circle_size, circle_speed, circle_offset, circle_start):
    pos = 0
    spd = 0.05
    decay = 6000
    circle_factor = circle_speed + circle_offset
    min_x = max_x = min_y = max_y = prev_x = prev_y = 400
    points = []
    for pos in range(decay//10, decay):
        adjx = int(400 + int(200 * (pos/float(decay)) * math.sin(pos * spd)))
        adjy = int(400 + int(200 * (pos/float(decay)) * math.sin(starter + (pos * spd * ratio))))
        adjx += int(circle_size * 200 * (pos/float(decay)) * math.sin(circle_start + (pos * spd * circle_factor)))
        adjy += int(circle_size * 200 * (pos/float(decay)) * math.cos(circle_start + (pos * spd * circle_factor)))
        points.append((adjx, adjy))
        min_x = min(min_x, adjx)
        min_y = min(min_y, adjy)
        max_x = max(max_x, adjx)
        max_y = max(max_y, adjy)

    scale = min(800.0/(max_x - min_x), 800.0/(max_y - min_y))
    x_offset = ((max_x + min_x)/2 - 400)*70/400
    y_offset = ((max_y + min_y)/2 - 400)*70/400


    # ser = serial.Serial('/dev/ttyACM0', 9600)
    # tosend = f'{ratio} {starter} {circle_size} {circle_factor} {circle_start} {x_offset} {y_offset} {scale:.4f}'
    # print(tosend)
    # ser.write(tosend.encode('utf-8'))

    image = svgwrite.Drawing(size=(800,800))
    image.add(Polyline(points=points, fill="none", stroke='black'))
    
    # for point in points:
    #     point_x = scale*(point[0] - min_x)
    #     point_y = scale*(point[1] - min_y)
    #     # image.line(prev_x, prev_y, point_x, point_y)
    #     prev_x, prev_y = point_x, point_y
    #     image.add(Line(start=(prev_x, prev_y), end=(point_x, point_y)))

    return image.tostring()

def random_image():
    params = {
    "ratio":float(random.randint(1, 3)) + random.uniform(-0.03, 0.03),
    "starter":random.uniform(0.0, 3.142),
    "circle_size":random.uniform(0.0, 1.0),
    "circle_speed":random.uniform(0.0, 3.0),
    "circle_offset":random.uniform(-0.05, 0.05),
    "circle_start":random.uniform(0.0, 3.142),
    }
    return params, harmonograph(**params)



@app.route('/', methods=['GET'])
def home():
    if 'ratio' in request.args:
        values = []
        for k in ['ratio', 'starter', 'circle_size', 'circle_speed', 'circle_offset', 'circle_start']:
            v =  request.args.get(k)
            values.append('%.7g' % float( v ))
        line = '{' + ', '.join(values) + '},\n'
        with open('values.txt', 'a') as f:
            f.write(line)

        return redirect('/')


    params, drawing = random_image()
    # return drawing
    url_params = '&'.join(f'{k}={v}' for k, v in params.items())
    return render_template("index.html", drawing=drawing, url_params=url_params)


if __name__ == '__main__':
    app.run()
