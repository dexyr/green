from enum import Enum

import data
from data import Position, Unit

from world_util import Map

import renderer


class Player:
    unit: Unit
    position: Position = Position(0, 0)

    def __init__(self, unit: Unit):
        self.unit = unit


class WorldStates(Enum):
    LOAD = 0
    WORLD = 1


class World:
    state = WorldStates.LOAD
    map: Map
    player: Player = Player(data.Globals.party[1])

    @classmethod
    def logic(cls) -> None:
        if cls.state == WorldStates.LOAD:
            cls.logic_load()
        if cls.state == WorldStates.WORLD:
            cls.logic_world()

        # place player somewhere
        # handle logic for keys etc.

    @classmethod
    def logic_load(cls) -> None:
        cls.map = Map(data.Constants.TEST_MAP)
        cls.state = WorldStates.WORLD

    @classmethod
    def logic_world(cls) -> None:
        pass

    @classmethod
    def render(cls) -> None:
        if cls.state == WorldStates.WORLD:
            cls.render_world()

    @classmethod
    def render_world(cls) -> None:
        # the camera position should be rendered at the center of the screen
        # this means that everything needs to be offset

        # maybe the camera should provide this offset
        offset_x: int =\
            cls.player.position.x + renderer.Constants.TERMINAL_WIDTH // 2
        offset_y: int =\
            cls.player.position.y + renderer.Constants.TERMINAL_HEIGHT // 2

        for y, r in enumerate(cls.map.blocks):
            for x, c in enumerate(r):
                renderer.draw_char(
                    offset_x + x, offset_y + y, c.char, c.color, 0)

        renderer.draw_unit(
            offset_x + cls.player.position.x,
            offset_y + cls.player.position.y,
            cls.player.unit,
            2)
