from typing import List, Dict
from enum import Enum
from dataclasses import dataclass


class GameStates(Enum):
    WORLD = 0
    BATTLE = 1


class Teams(Enum):
    PLAYER = 0
    ENEMY = 1


class Position:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class BlockType:
    char: str
    color: str
    solid: bool

    def __init__(self, char: str, color: str, solid: bool):
        assert len(char) == 1

        self.char = char
        self.color = color
        self.solid = solid


class BlockTypes:
    GROUND: BlockType = BlockType('.', 'grey', False)
    WALL: BlockType = BlockType('x', 'white', True)
    BARREL: BlockType = BlockType('o', 'darker amber', True)
    WATER: BlockType = BlockType('~', 'dark blue', False)


class AttackType:
    def __init__(self, name: str, damage: int, delay: int):
        self.name: str = name
        self.damage: int = damage
        self.delay: int = delay


class AttackTypes:
    BASIC_ATTACK: AttackType = AttackType(
        'basic attack', 2, 2)

    DAGGER_THROW: AttackType = AttackType(
        'dagger throw', 1, 4)

    HEAVY_ATTACK: AttackType = AttackType(
        'heavy attack', 3, 6)

    ARROW: AttackType = AttackType(
        'arrow', 3, 4)

    FIREBALL: AttackType = AttackType(
        'fireball', 4, 8)

    BOUNCE: AttackType = AttackType(
        'bounce', 2, 3)


class Attack:
    def __init__(self, attack_type: AttackType):
        self.attack_type: AttackType = attack_type


class UnitType:
    def __init__(
            self, name: str, team: Teams, char: str, color: str, hp_base: int,
            speed_base: int, attacks_base: List[AttackType],
            target_types: List[str]):

        if len(char) > 1:
            raise Exception('Unit.char should be a single character')

        self.name: str = name
        self.team: Teams = team
        self.char: str = char
        self.color: str = color
        self.hp_base: int = hp_base
        self.speed_base: int = speed_base
        self.attacks_base: List[AttackType] = attacks_base

        # todo: figure out what polymorphic implementation to use
        self.target_types: List[str] = target_types


class UnitTypes:
    TANK: UnitType = UnitType(
        name='tank',
        team=Teams.PLAYER,
        char='t',
        color='dark amber',
        hp_base=18,
        speed_base=3,
        attacks_base=[AttackTypes.HEAVY_ATTACK],
        target_types=[])

    FIGHTER: UnitType = UnitType(
        name='fighter',
        team=Teams.PLAYER,
        char='f',
        color='dark flame',
        hp_base=14,
        speed_base=7,
        attacks_base=[AttackTypes.BASIC_ATTACK, AttackTypes.DAGGER_THROW],
        target_types=[])

    RANGER: UnitType = UnitType(
        name='ranger',
        team=Teams.PLAYER,
        char='r',
        color='dark sea',
        hp_base=10,
        speed_base=9,
        attacks_base=[AttackTypes.ARROW],
        target_types=[])

    MAGE: UnitType = UnitType(
        name='mage',
        team=Teams.PLAYER,
        char='m',
        color='dark azure',
        hp_base=6,
        speed_base=5,
        attacks_base=[AttackTypes.FIREBALL],
        target_types=[])

    SLIME: UnitType = UnitType(
        name='slime',
        team=Teams.ENEMY,
        char='s',
        color='cyan',
        hp_base=5,
        speed_base=5,
        attacks_base=[AttackTypes.BOUNCE],
        target_types=['tank', 'fighter', 'ranger', 'mage'])


@dataclass
class Unit:
    def __init__(self, unit_type: UnitType):
        self.unit_type: UnitType = unit_type
        self.hp: int = unit_type.hp_base
        self.speed: int = unit_type.speed_base

        self.attacks: List[Attack] = []
        for a in unit_type.attacks_base:
            self.attacks.append(Attack(a))

        self.battle_delay: int = 0


class Constants:
    TEST_MAP: List[str] = [
        'xxx..xxx',
        'x......x',
        'x.o....x',
        'xo.....x',
        'xo.....x',
        'x...ww.x',
        'x...ww.x',
        'xxx..xxx']

    STRING_MAP_MAP: Dict[str, BlockType] = {
        '.': BlockTypes.GROUND,
        'x': BlockTypes.WALL,
        'o': BlockTypes.BARREL,
        'w': BlockTypes.WATER}


class Globals:
    state: GameStates
    keys: List[int] = []

    party: List[Unit] = [
        Unit(UnitTypes.TANK),
        Unit(UnitTypes.FIGHTER),
        Unit(UnitTypes.RANGER),
        Unit(UnitTypes.MAGE)]

    enemies: List[Unit] = [
        Unit(UnitTypes.SLIME),
        Unit(UnitTypes.SLIME)]
