import numpy
from math import pi, inf, isinf, sqrt, cos, tan

from dataclasses import dataclass
from typing import List, Optional

from Point import *


__all__ = ['CalculatorInputData', 'ClosestPointsCalculator']


@dataclass
class Line:
    slope: float
    intercept: float=0

    @property
    def is_slope_inf(self) -> bool:
        return isinf(self.slope)

    def __repr__(self) -> str:
        if self.is_slope_inf:
            return f'x = {self.intercept}'
        else:
            result = 'y = '

            if self.slope == 0:
                result += f'{self.intercept}'
            else:
                result += f'{self.slope}x'

                if self.intercept > 0:
                    result += f' + {self.intercept}'
                if self.intercept < 0:
                    result += f' - {abs(self.intercept)}'

        return result


@dataclass
class Vector:
    initial_point: Point
    terminal_point: Point


@dataclass
class CalculatorInputData:
    cur_pos: Point
    prev_pos: Point
    abs_angle: float
    angle_to_road: float
    dist: float


class ClosestPointsCalculator:
    __precision: int=6
    __input_data: CalculatorInputData=None
    __bot_line: Optional[Line]
    __road_lines: List[Line]
    __closest_point: Optional[Point]

    def get_closest_point(self, input_data: CalculatorInputData) -> Optional[Point]:
        if input_data.prev_pos is not None:
            self.__input_data = input_data

            self.__bot_line = None
            self.__road_lines = []
            self.__closest_point = None

            self.__calculate_bot_line()
            self.__calculate_road_lines()
            self.__calculate_closest_point()

            return self.__closest_point

        return None

    def __calculate_bot_line(self) -> None:
        slope = self.__my_tan(self.__input_data.abs_angle)
        self.__bot_line = Line(slope=slope)

        if self.__bot_line.is_slope_inf:
            self.__bot_line.intercept = self.__input_data.cur_pos.x
        else:
            self.__bot_line.intercept = self.__input_data.cur_pos.y - self.__bot_line.slope * self.__input_data.cur_pos.x

    def __calculate_road_lines(self) -> None:
        self.__road_lines = []

        slope = self.__get_slope_of_road_lines()
        intercept_values = self.__get_intercept_of_road_lines(slope=slope)

        for intercept in intercept_values:
            cur_road_line = Line(slope=slope, intercept=intercept)

            self.__road_lines.append(cur_road_line)

    def __calculate_closest_point(self) -> None:
        if self.__input_data.prev_pos is not None:
            closest_points = []
            vector_of_moving = Vector(
                initial_point=self.__input_data.prev_pos,
                terminal_point=self.__input_data.cur_pos
            )

            for line in self.__road_lines:
                x = self.__get_x_of_closest_point(road_line=line)
                y = self.__get_y_of_closest_point(road_line=line, closest_x=x)

                cur_point = Point(x, y)

                closest_points.append(cur_point)

            for point in closest_points:
                point_pos_relative_to_vector = self.__point_position_relative_to_vector(
                    vector=vector_of_moving,
                    point=point
                )

                is_point_appropriate = point_pos_relative_to_vector * numpy.sign(self.__input_data.dist) < 0

                if is_point_appropriate:
                    self.__closest_point = point

    def __get_slope_of_road_lines(self) -> float:
        if self.__bot_line.is_slope_inf:
            if self.__is_zero(self.__input_data.angle_to_road):
                return inf
            else:
                abs_of_new_angle = abs(pi / 2) - abs(self.__input_data.angle_to_road)

                sign_of_new_angle = numpy.sign(-self.__input_data.angle_to_road)

                new_angle = sign_of_new_angle * abs_of_new_angle

                return self.__my_tan(new_angle)
        else:
            if self.__is_tan_of_angle_inf(angle=self.__input_data.angle_to_road):
                return self.__my_divide(-1, self.__bot_line.slope)
            else:
                a = tan(self.__input_data.angle_to_road)
                s = self.__bot_line.slope

                return self.__my_divide(a + s, 1 - a * s)

    def __get_intercept_of_road_lines(self, slope: float) -> List[float]:
        if isinf(slope):
            intercept1 = self.__input_data.cur_pos.x - self.__input_data.dist
            intercept2 = self.__input_data.cur_pos.x + self.__input_data.dist

            return [intercept1, intercept2]
        else:
            a = slope
            x = self.__input_data.cur_pos.x
            y = self.__input_data.cur_pos.y
            r = self.__input_data.dist ** 2

            A = 1
            B = 2 * (a * x - y)
            C = a ** 2 * (x ** 2 - r ** 2) - y * (2 * slope * x - y) - r

            return self.__solve_quadratic_equation(a=A, b=B, c=C)

    def __get_x_of_closest_point(self, road_line: Line) -> float:
        if road_line.is_slope_inf:
            return road_line.intercept
        else:
            A = road_line.slope ** 2 + 1
            B = road_line.slope * (road_line.intercept - self.__input_data.cur_pos.y) - self.__input_data.cur_pos.x

            return -B / A

    def __get_y_of_closest_point(self, road_line: Line, closest_x: float) -> float:
        if road_line.is_slope_inf:
            return self.__input_data.cur_pos.y
        else:
            return road_line.slope * closest_x + road_line.intercept

    @staticmethod
    def __point_position_relative_to_vector(vector: Vector, point: Point) -> Optional[float]:
        ax = vector.initial_point.x
        ay = vector.initial_point.y

        bx = vector.terminal_point.x
        by = vector.terminal_point.y

        px = point.x
        py = point.y

        result = (bx - ax) * (py - ay) - (by - ay) * (px - ax)

        # result < 0 - right
        # result > 0 - left

        return numpy.sign(result)

    @staticmethod
    def __solve_quadratic_equation(a: float, b: float, c: float) -> List[float]:
        D = b ** 2 - 4 * a * c

        x1 = (-b - sqrt(D)) / (2 * a)
        x2 = (-b + sqrt(D)) / (2 * a)

        return [x1, x2]

    def __my_round(self, number: float) -> float:
        return round(number, self.__precision)

    def __is_zero(self, number) -> bool:
        return self.__my_round(number) == 0

    def __my_divide(self, numerator: float, denominator: float) -> float:
        if self.__is_zero(denominator):
            return inf

        return numerator / denominator

    def __my_tan(self, angle: float) -> float:
        if self.__is_zero(cos(angle)):
            return inf

        return tan(angle)

    def __is_tan_of_angle_inf(self, angle: float) -> bool:
        return isinf(self.__my_tan(angle))
