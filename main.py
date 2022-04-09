from math import inf

from pyglet.window import key
from pyglet import clock, app

from Point import *
from Graph import *
from config import *
from Drivers import *
from GraphDrawer import *
from ClosestPointsCalculator import *
from gym_duckietown.envs.duckietown_env import DuckietownEnv


global prev_pos, environment, key_handler, graph, drawer, calculator, driver

graph: Graph
environment: DuckietownEnv
key_handler: key.KeyStateHandler
graph: Graph
drawer: GraphDrawer
calculator: ClosestPointsCalculator
driver: Driver


def init_global_vars():
    global prev_pos, environment, key_handler, graph, drawer, calculator, driver

    prev_pos = None

    environment = DuckietownEnv(
        seed=MAP_SEED,
        map_name=MAP_NAME,
        domain_rand=False,
        max_steps=inf,
    )
    environment.reset()
    environment.render()

    key_handler = key.KeyStateHandler()
    environment.unwrapped.window.push_handlers(key_handler)

    if DRIVING_TYPE == 'auto':
        driver = AutoDriver(environment=environment)
    if DRIVING_TYPE == 'manual':
        driver = ManualDriver(key_handler=key_handler, environment=environment)

    graph = Graph(min_distance=MIN_DISTANCE_IN_GRAPH)

    calculator = ClosestPointsCalculator()

    key_to_close = key.symbol_string(KEY_TO_CLOSE_GRAPH).lower()
    drawer_settings = GraphDrawerSettings(
        key_to_close=key_to_close,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        min_x=GRAPH_MIN_X,
        max_x=GRAPH_MAX_X,
        min_y=GRAPH_MIN_Y,
        max_y=GRAPH_MAX_Y,
        roads_color=ROADS_COLOR,
        thickness=ROADS_THICKNESS,
        bg_color=BACKGROUND_COLOR,
        radius=NODES_RADIUS,
        margin=MARGIN,
        nodes_color=NODES_COLOR,
    )
    drawer = GraphDrawer(drawer_settings)


def get_data_for_calculator() -> CalculatorInputData:
    global prev_pos

    lane_pose = environment.get_lane_pos2(environment.cur_pos, environment.cur_angle)

    cur_x = environment.cur_pos[0]
    cur_y = environment.cur_pos[2]
    cur_pos = Point(cur_x, cur_y)

    absolute_angle = environment.cur_angle
    angle_to_road = lane_pose.angle_rad
    distance_to_road = lane_pose.dist

    result = CalculatorInputData(
        cur_pos=cur_pos,
        prev_pos=prev_pos,
        abs_angle=absolute_angle,
        angle_to_road=angle_to_road,
        dist=distance_to_road
    )

    prev_pos = cur_pos

    return result


init_global_vars()


def update(dt):
    input_data = get_data_for_calculator()

    closest_point = calculator.get_closest_point(input_data)

    graph.check(closest_point)

    if key_handler[KEY_TO_SHOW_GRAPH]:
        key_handler[KEY_TO_SHOW_GRAPH] = False

        drawer.upload_graph(graph)

        drawer.show_graph()

    _, _, done, _ = environment.step(driver.action)

    if done:
        environment.reset()
        environment.render()

    environment.render()


clock.schedule_interval(update, 1.0 / environment.unwrapped.frame_rate)

app.run()

environment.close()
