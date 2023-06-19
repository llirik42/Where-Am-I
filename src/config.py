from pyglet.window import key


__all__ = [
    'DRIVING_TYPE',
    'IMAGE_WIDTH',
    'IMAGE_HEIGHT',
    'MIN_DISTANCE_IN_GRAPH',
    'KEY_TO_SHOW_GRAPH',
    'KEY_TO_CLOSE_GRAPH',
    'MAP_SEED',
    'MAP_NAME',
    'MARGIN',
    'NODES_RADIUS',
    'NODES_COLOR',
    'ROADS_COLOR',
    'ROADS_THICKNESS',
    'BACKGROUND_COLOR',
    'GRAPH_MIN_X',
    'GRAPH_MAX_X',
    'GRAPH_MIN_Y',
    'GRAPH_MAX_Y'
]

# Тип вождения, "auto" - бот сам будет ездить, "manual" - ручное управлние ботом
DRIVING_TYPE = 'auto'

# Ширина окна с графом
IMAGE_WIDTH = 600

# Высота окна с графов
IMAGE_HEIGHT = 600

# Минимальное расстояние между узлами в графе
MIN_DISTANCE_IN_GRAPH = 0.01

# Клавиша, нужная, чтобы показать окно с графом
KEY_TO_SHOW_GRAPH = key.Q

# Клавиша, нужная, чтобы закрыть окно с графом
KEY_TO_CLOSE_GRAPH = key.E

# Сид карты, влияет на начальное положение бота
MAP_SEED = 1

# Название карты. Все возможные карты лежат в ./src/maps (указывать без '.yaml')
MAP_NAME = 'udem1'

# Отступ от края в графическом представлении графа
MARGIN = 10

# Радиус узлов в графическом представлении графа
NODES_RADIUS = 10

# Ширина дорог в графическом представлении графа
ROADS_THICKNESS = 5

# Цвет узлов в графическом представлении графа
NODES_COLOR = (255, 255, 255)

# Цвет дорог в графическом представлении графа
ROADS_COLOR = (255, 255, 255)

# Цвет заднего фона в графическом представлении графа
BACKGROUND_COLOR = (0, 0, 0)

# Минимальное значание "x" в графе
GRAPH_MIN_X = None

# Максимальное значание "x" в графе
GRAPH_MAX_X = None

# Минимальное значание "y" в графе
GRAPH_MIN_Y = None

# Максимальное значание "y" в графе
GRAPH_MAX_Y = None
