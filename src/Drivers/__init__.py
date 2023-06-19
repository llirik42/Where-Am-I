from math import pi

import numpy
from pyglet.window import key

from gym_duckietown.src.gym_duckietown.simulator import LanePosition
from gym_duckietown.src.gym_duckietown.envs.duckietown_env import DuckietownEnv


__all__ = ['Driver', 'ManualDriver', 'AutoDriver']


class Driver:
    _environment: DuckietownEnv
    _speed: float=0
    _rotation: float=0

    def __init__(self, environment: DuckietownEnv) -> None:
        self._environment = environment

    @property
    def action(self) -> numpy.ndarray:
        self._speed = 0
        self._rotation = 0

        self._update_speed()
        self._update_rotation()

        return numpy.array([self._speed, self._rotation])

    def _update_speed(self) -> None:
        pass

    def _update_rotation(self) -> None:
        pass


class ManualDriver(Driver):
    def __init__(self, environment: DuckietownEnv, key_handler: key.KeyStateHandler) -> None:
        super().__init__(environment=environment)

        self.__key_handler = key_handler

    def _update_speed(self) -> None:
        max_speed = 0.44

        is_moving_forward = self.__key_handler[key.UP] or self.__key_handler[key.W]
        is_moving_back = self.__key_handler[key.DOWN] or self.__key_handler[key.S]

        self._speed = max_speed * (is_moving_forward - is_moving_back)

    def _update_rotation(self) -> None:
        max_rotation = 1

        is_moving_left = self.__key_handler[key.LEFT] or self.__key_handler[key.A]
        is_moving_right = self.__key_handler[key.RIGHT] or self.__key_handler[key.D]

        self._rotation = max_rotation * (is_moving_left - is_moving_right)


class AutoDriver(Driver):
    def __init__(self, environment: DuckietownEnv) -> None:
        super().__init__(environment=environment)

    def _update_speed(self) -> None:
        abs_delta_angle = abs(1 - 2 * abs(self.__angle_to_road) / pi)

        self._speed = self.__get_dependence(
            value=abs_delta_angle,
            power=5,
            multiplier=0.35
        )

    def _update_rotation(self) -> None:
        self.__update_rotation_by_angle_to_road()

        self.__update_rotation_by_distance_to_road()

    def __update_rotation_by_angle_to_road(self) -> None:
        self._rotation += self.__get_dependence(
            value=self.__angle_to_road / pi,
            power=0.45,
            multiplier=6
        )

    def __update_rotation_by_distance_to_road(self) -> None:
        self._rotation += self.__get_dependence(
            value=self.__distance_to_road,
            power=0.7,
            multiplier=6
        )

    @property
    def __distance_to_road(self) -> float:
        return self.__lane_pos.dist + 0.14

    @property
    def __angle_to_road(self) -> float:
        return self.__lane_pos.angle_rad

    @property
    def __lane_pos(self) -> LanePosition:
        return self._environment.get_lane_pos2(self._environment.cur_pos, self._environment.cur_angle)

    @staticmethod
    def __get_dependence(value: float, power: float, multiplier: float) -> float:
        return abs(value) ** power * numpy.sign(value) * multiplier
