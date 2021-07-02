from talon import Module, Context, canvas, ctrl, cron, ui, actions, app
from talon.types import Point2d

from math import atan2, sin, cos, pi
import time
from random import randrange, normalvariate, choice

racer = Module()

racer_turns_cw = True
racer_speed = 0.0
racer_turning = False

racer_turn_start_time = 0

racer_position = Point2d(0, 0)
racer_angle    = 0.0

racer_tick_job = None

racer_random_mode = False

last_input_time = 0

def had_input():
    global last_input_time
    last_input_time = time.time()

racer.list("point_of_compass", desc="point of compass for race car")

ctx = Context()

direction_name_steps = [
        "east", "east south east", "south east", "south south east",
        "south", "south south west", "south west", "west south west",
        "west", "west north west", "north west", "north north west",
        "north", "north north east", "north east", "east north east" ] 

ctx.lists["self.point_of_compass"] = {
            word: str(idx * pi * 2 / len(direction_name_steps)) for (idx, word) in enumerate(direction_name_steps)
        } 

print(ctx.lists["self.point_of_compass"])

def racer_tick_cb():
    global racer_position
    global racer_angle

    global racer_turning
    global racer_turns_cw

    if racer_random_mode:
        if racer_turning == False and randrange(0, 1000) < 10:
            racer_turning = max(0, normalvariate(1, 0.3))
            racer_turns_cw = choice([True, False])
        if racer_turning != False and randrange(0, 1000) < 15:
            racer_turns_cw = normalvariate(5, 2) * choice([-1, 1])

    if isinstance(racer_turning, float):
        racer_turning -= 1 / 40
        if racer_turning <= 0:
            racer_turning = False

    if isinstance(racer_turns_cw, float):
        if racer_turns_cw < 0:
            racer_turns_cw += 1 / 40
            if racer_turns_cw >= 0:
                racer_turns_cw = False
        else:
            racer_turns_cw -= 1 / 40
            if racer_turns_cw >= 0:
                racer_turns_cw = True

    if racer_speed > 0.0 or racer_turning:
        racer_position += Point2d(cos(racer_angle), sin(racer_angle)) * racer_speed * 5
        racer_canvas.move(racer_position.x, racer_position.y)
        real_pos = racer_position + Point2d(128, 128)
        ctrl.mouse_move(real_pos.x, real_pos.y)
        if racer_turning and racer_turn_start_time < time.time() - 0.1:
            if racer_turns_cw:
                racer_angle -= 0.07
            else:
                racer_angle += 0.07
        racer_canvas.show()


        if real_pos.x < 0:
            racer_angle = vertical_edge_change_angle(racer_angle, True)
            racer_position.x = -128 # avoid geting stuck at edge
        if real_pos.x >= ui.screens()[0].rect.width:
            racer_angle = vertical_edge_change_angle(racer_angle, False)
            racer_position.x = ui.screens()[0].rect.width - 1 - 128
        if real_pos.y < 0:
            racer_angle = horizontal_edge_change_angle(racer_angle, True)
            racer_position.y = -128
        if real_pos.y >= ui.screens()[0].rect.height:
            racer_angle = horizontal_edge_change_angle(racer_angle, False)
            racer_position.y = ui.screens()[0].rect.height - 1 - 128

    if last_input_time + 45 < time.time():
        if racer_random_mode:
            if choice([True, False, False, False, False, False, False]):
                actions.user.racer_stop()
        else:
            actions.user.racer_stop()
            app.notify("car stopped after 45s of inactivity")

racer_canvas = None

def racer_canvas_draw(canvas):
    paint = canvas.paint

    paint.color = "00000000"

    canvas.translate(128, 128)
    canvas.translate(canvas.x, canvas.y)

    xpx = cos(-racer_angle + pi/2)
    ypx = -sin(-racer_angle + pi/2)

    xpy = sin(-racer_angle + pi/2)
    ypy = cos(-racer_angle + pi/2)

    paint.color = "ff0000ff"
    paint.stroke_width = 4
    canvas.draw_points(canvas.PointMode.POLYGON,
            [Point2d(0, 0),
                Point2d(-16 * xpx + -32 * xpy, -16 * ypx + -32 * ypy),
                Point2d(-20 * xpy, -20 * ypy),
                Point2d(16 * xpx - 32 * xpy, 16 * ypx - 32 * ypy),
                Point2d(0, 0)])

    direction = 1 if racer_turns_cw else -1

    canvas.draw_line(-4 * xpy, -4 * ypy, 16 * xpx * direction - 8 * xpy, 16 * ypx * direction - 8 * ypy)

def vertical_edge_change_angle(angle : float, left : bool) -> float:
    """Change the angle after colliding with vertical edge"""
    dx = cos(angle)
    dy = sin(angle)
    if left and dx < 0 or not left and dx > 0:
        dx = - dx
        angle = atan2(dy, dx)
    return angle

def horizontal_edge_change_angle(angle : float, top : bool) -> float:
    """Change the angle after colliding with horizontal edge"""
    dx = cos(angle)
    dy = sin(angle)
    #print('dx ' + str(dx) + ' dy: ' + str(dy) + ' old angle: ' + str(angle))
    if top and dy < 0 or not top and dy > 0:
        dy = - dy
        angle = atan2(dy, dx)

    #print('new angle: ' + str(angle))
    return angle

@racer.action_class
class RacerActions:
    def racer_start():
        """Starts the "racing" mouse mode"""
        global racer_canvas
        global racer_position
        global racer_tick_job
        global racer_speed
        had_input()
        print("vroom vroom")
        if racer_canvas is None:
            racer_canvas = canvas.Canvas(0, 0, 256, 256)
        racer_position = Point2d(ui.screens()[0].rect.width / 2, ui.screens()[0].rect.height / 2)
        # racer_position = Point2d(5, 5)
        racer_canvas.register("draw", racer_canvas_draw)
        if racer_tick_job:
            cron.cancel(racer_tick_job)
        racer_tick_job = cron.interval("40ms", racer_tick_cb)
        racer_canvas.show()
        # racer_canvas.freeze()

    def racer_stop():
        """Stops the "racing" mouse mode"""
        print("no longer vroom vroom")
        cron.cancel(racer_tick_job)
        racer_canvas.unregister("draw", racer_canvas_draw)
        racer_canvas.hide()

    def racer_random(activate: int = -1):
        """Activate or deactivate or toggle the random turn mode"""
        global racer_random_mode
        had_input()
        if activate == -1:
            racer_random_mode = not racer_random_mode
        else:
            racer_random_mode = activate != 0
        if racer_random_mode:
            actions.user.racer_gas_toggle()

    def racer_set_direction(direction: str):
        """Set the direction to a value in radians"""
        global racer_angle
        had_input()
        print("setting direction to ", direction)
        racer_angle = (float(direction)*(2*pi/360)) - pi/2
        
    def racer_turn_start():
        """Starts turning the "car"."""
        global racer_turning
        global racer_turn_start_time
        racer_turn_start_time = time.time()
        had_input()
        print("turning...")
        racer_turning = True

    def racer_turn_stop():
        """Stops turning the "car"."""
        global racer_turning
        had_input()
        if racer_turn_start_time >= time.time() - 0.1:
            actions.user.racer_flip_turn_direction()
        else:
            print("straight ahead")
        racer_turning = False

    def racer_flip_turn_direction():
        """Changes rotation from CW to CCW and back"""
        global racer_turns_cw
        had_input()
        racer_turns_cw = not racer_turns_cw
        print("racer turning ", racer_turns_cw and "clockwise" or "counterclockwise")

    def racer_nudge():
        """Drives the car forward a tiny bit"""
        global racer_speed
        had_input()
        racer_speed = 0.1
        def reset():
            global racer_speed
            racer_speed = 0.0
        cron.after("500ms", reset)

    def racer_gas_toggle():
        """Switch between driving and stopped"""
        global racer_speed
        had_input()
        if racer_speed == 0.0:
            racer_speed = 1.0
        else:
            racer_speed = 0.0

    def racer_turbo_toggle():
        """Switch between driving TURBO DRIVING"""
        global racer_speed
        had_input()
        if racer_speed == 1.0:
            racer_speed = 5.0
        else:
            racer_speed = 1.0

    def racer_reverse():
        """Turn the racer around 180 degrees"""
        global racer_angle
        racer_angle += pi
        had_input()
