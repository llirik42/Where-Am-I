from dataclasses import dataclass
from typing import List, Optional

from config import MIN_DISTANCE_IN_GRAPH
from Point import Point


__all__ = ['Graph', 'RoadStretch']


@dataclass
class Node:
    center: Point


@dataclass
class RoadStretch:
    node_1: Node
    node_2: Node


class Graph:
    __nodes: List[Node]=[]
    __stretches: List[RoadStretch]=[]
    __cur_index: int=-1
    __prev_index: int=-1

    def __init__(self, min_distance: float=MIN_DISTANCE_IN_GRAPH) -> None:
        self.__min_distance = min_distance

    @property
    def nodes(self) -> List[Node]:
        return self.__nodes

    @property
    def stretches(self) -> List[RoadStretch]:
        return self.__stretches

    @property
    def number_of_nodes(self) -> int:
        return len(self.__nodes)

    def check(self, pos_of_node: Optional[Point]) -> None:
        if pos_of_node is not None:
            node_to_check = Node(pos_of_node)

            index_of_nearest = self.__get_index_of_nearest(node_to_check)

            nearest_node = None if index_of_nearest == -1 else self.__nodes[index_of_nearest]

            is_node_appropriate = index_of_nearest == -1 or nearest_node.center - node_to_check.center >= self.__min_distance

            if is_node_appropriate:
                self.__add_node(node_to_check)
            else:
                self.__prev_index = self.__cur_index
                self.__cur_index = index_of_nearest

            if len(self.__nodes) > 1:
                self.__link_prev_and_cur()

    @property
    def __is_graph_empty(self) -> bool:
        return self.number_of_nodes == 0

    def __get_index_of_nearest(self, node: Node) -> int:
        index = -1

        if not self.__is_graph_empty:
            distance = self.__nodes[0].center - node.center
            index = 0

            for cur_index in range(1, len(self.__nodes)):
                cur_dist = self.__nodes[cur_index].center - node.center

                if cur_dist < distance:
                    distance = cur_dist
                    index = cur_index

        return index

    def __add_node(self, node: Node) -> None:
        if self.__is_graph_empty:
            self.__prev_index = 0
        else:
            self.__prev_index = self.__cur_index

        self.__cur_index = len(self.__nodes)

        self.__nodes.append(node)

    def __link_prev_and_cur(self) -> None:
        new_stretch = RoadStretch(
            node_1=self.__nodes[self.__cur_index],
            node_2=self.__nodes[self.__prev_index],
        )

        self.__stretches.append(new_stretch)

    def __repr__(self) -> str:
        return f'Nodes: {self.__nodes}'
