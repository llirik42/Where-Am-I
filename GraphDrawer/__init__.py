import numpy
import cv2
from dataclasses import dataclass
from pyglet.window import key
from typing import Tuple, Optional

from Graph import Graph, RoadStretch
from Point import Point
from config import *


__all__ = ['GraphDrawerSettings', 'GraphDrawer']


Image = numpy.ndarray

Color = Tuple[int, int, int]


@dataclass
class GraphDrawerSettings:
    min_x: Optional[float]=None
    max_x: Optional[float]=None
    min_y: Optional[float]=None
    max_y: Optional[float]=None
    width: int=IMAGE_WIDTH
    height: int=IMAGE_HEIGHT
    margin: int=MARGIN
    radius: int=NODES_RADIUS
    thickness: int=ROADS_THICKNESS
    nodes_color: Color=NODES_COLOR
    roads_color: Color=ROADS_COLOR
    bg_color: Color=BACKGROUND_COLOR
    key_to_close: str=key.symbol_string(KEY_TO_CLOSE_GRAPH).lower()


class GraphDrawer:
    __settings: GraphDrawerSettings
    __SCALING_CONSTANT: int
    __min_x: float
    __max_x: float
    __min_y: float
    __max_y: float
    __graph: Graph
    __width: int
    __height: int
    __image: Image=None

    def __init__(self, settings: GraphDrawerSettings) -> None:
        self.__settings = settings
        self.__width = self.__settings.width
        self.__height = self.__settings.height

        self.__SCALING_CONSTANT = self.__settings.margin + self.__settings.radius

    @property
    def image(self) -> Image:
        return self.__image

    def upload_graph(self, graph: Graph) -> None:
        self.__graph = graph

        self.__init_image()

        if self.__graph.number_of_nodes != 0:
            self.__calculate_min_max_x_y()

            self.__draw_nodes()

            self.__draw_roads()

    def show_graph(self) -> None:
        if self.__image is not None:
            cv2.imshow(winname=' ', mat=self.__image)

            while True:
                if cv2.waitKey(0) & 0xFF == ord(self.__settings.key_to_close):
                    break

            cv2.destroyWindow(' ')

    def __init_image(self) -> None:
        self.__image = numpy.zeros(shape=(self.__height, self.__width), dtype=numpy.uint8)

    def __calculate_min_max_x_y(self) -> None:
        self.__min_x = self.__settings.min_x
        self.__max_x = self.__settings.max_x

        self.__min_y = self.__settings.min_y
        self.__max_y = self.__settings.max_y

        if self.__min_x is None or self.__max_x is None:
            x_values = [node.center.x for node in self.__graph.nodes]

            if self.__min_x is None:
                self.__min_x = min(x_values)
            if self.__max_x is None:
                self.__max_x = max(x_values)

        if self.__min_y is None or self.__max_y is None:
            y_values = [node.center.y for node in self.__graph.nodes]

            if self.__min_y is None:
                self.__min_y = min(y_values)
            if self.__max_y is None:
                self.__max_y = max(y_values)

    def __draw_nodes(self) -> None:
        if len(self.__graph.nodes) == 1:
            self.__draw_circle(center=Point(
                x=self.__width // 2,
                y=self.__height // 2,
            ))
        else:
            for node in self.__graph.nodes:
                scaled_center = self.__scale_point(point=node.center)

                self.__draw_circle(center=scaled_center)

    def __draw_roads(self) -> None:
        for stretch in self.__graph.stretches:
            self.__draw_stretch(stretch)

    def __scale_point(self, point: Point) -> Point:
        scaled_x = self.__scale_x(value=point.x)
        scaled_y = self.__scale_y(value=point.y)

        return Point(x=scaled_x, y=scaled_y)

    def __scale_x(self, value: float) -> int:
        if self.__max_x != self.__min_x:
            return self.__SCALING_CONSTANT + int(self.__scale(
                value=value,
                from_low=self.__min_x,
                from_high=self.__max_x,
                to_low=0,
                to_high=self.__width - 2 * self.__SCALING_CONSTANT,
            ))

        return self.__width // 2

    def __scale_y(self, value: float) -> int:
        if self.__min_y != self.__max_y:
            return self.__SCALING_CONSTANT + int(self.__scale(
                value=value,
                from_low=self.__min_y,
                from_high=self.__max_y,
                to_low=0,
                to_high=self.__height - 2 * self.__SCALING_CONSTANT,
            ))

        return self.__height // 2

    def __draw_stretch(self, stretch: RoadStretch) -> None:
        pt_1 = self.__scale_point(point=stretch.node_1.center)
        pt_2 = self.__scale_point(point=stretch.node_2.center)

        cv2.line(
            img=self.__image,
            pt1=pt_1.tuple,
            pt2=pt_2.tuple,
            color=self.__settings.roads_color,
            thickness=self.__settings.thickness
        )

    def __draw_circle(self, center: Point) -> None:
        cv2.circle(
            img=self.__image,
            center=center.tuple,
            radius=self.__settings.radius // 2,
            color=self.__settings.nodes_color,
            thickness=self.__settings.radius
        )

    @staticmethod
    def __scale(value, from_low: float, from_high: float, to_low: float, to_high: float) -> Optional[float]:
        if from_low != from_high and to_high != to_low:
            return (to_high - to_low) * (value - from_low) / (from_high - from_low) + to_low
        else:
            return None
