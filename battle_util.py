"""
this is the 'toybox' full of battle data
"""

from typing import List, Callable, Optional

# these are only for menu navigation
from bearlibterminal.terminal import TK_UP, TK_DOWN, TK_LEFT, TK_RIGHT

import renderer
from data import Position, Unit, Attack, Teams
from renderer import GraphicBlock


class BattlePosition:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.unit: Optional[Unit] = None


class TimelinePoint:
    def __init__(self, x: int):
        self.x: int = x
        self.units: List[Unit] = []


# for now, using this jank system of addressing, plus it opens up the ability
#   for some silly algorithmic operations
#
# ╔═╗     ╔═╗
# ║0║     ║4║
# ╠═╣     ╠═╣
# ║1║ ╔═╗ ║5║
# ╠═╣ ║ ║ ╠═╣
# ║2║ ╚═╝ ║6║
# ╠═╣     ╠═╣
# ║3║     ║7║
# ╚═╝     ╚═╝

class Constants:
    ACTIONS: List[str] = ['attack', 'move', 'use item', 'retreat']

    GRAPHIC_TIMELINE: List[str] = [
        '0 1 2 3 4 5 6 7 8 9 10  ',
        '├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼──┤']

    GRAPHIC_BATTLE: List[str] = [
        '╔═╗     ╔═╗',
        '║ ║     ║ ║',
        '╠═╣     ╠═╣',
        '║ ║ ╔═╗ ║ ║',
        '╠═╣ ║ ║ ╠═╣',
        '║ ║ ╚═╝ ║ ║',
        '╠═╣     ╠═╣',
        '║ ║     ║ ║',
        '╚═╝     ╚═╝']

    SIZE_SIDES: int = 4
    LENGTH_TEXT: int = 30

    GRAPHIC_MENU: List[str] = [
        '┌────────────────────────────┐',
        '│                            │',
        '│                            │',
        '│                            │',
        '│                            │',
        '│                            │',
        '└────────────────────────────┘']

    GRAPHIC_SELECT_POSITION: List[str] = [
        '╔═╗',
        '║ ║',
        '╚═╝']

    MENU_ANCHORS: List[Position] = [
        Position(2, 2),
        Position(2 + len('basic attack  '), 2),
        Position(2, 4),
        Position(2 + len('basic attack  '), 4)]

    OFFSET_TIMELINE_Y: int = 16
    OFFSET_MENU_Y: int = 40

    COLOR_FIELD: str = 'darkest grey'  # 'black'
    COLOR_SELECT: str = 'darker grey'


class Menu:
    block_menu: GraphicBlock = GraphicBlock(Constants.GRAPHIC_MENU)
    anchors: List[Position] = Constants.MENU_ANCHORS

    # helper
    @classmethod
    def get_new_selection(cls, key: int, index: int, count_items: int) -> int:
        index_new: int = cls.get_new_index(key, index)

        if index_new != -1 and index_new < count_items:
            return index_new

        return index

    @classmethod
    def get_new_index(cls, key: int, index: int) -> int:
        if key == TK_UP and index in [2, 3]:
            return index - 2

        if key == TK_DOWN and index in [0, 1]:
            return index + 2

        if key == TK_LEFT and index in [1, 3]:
            return index - 1

        if key == TK_RIGHT and index in [0, 2]:
            return index + 1

        return -1

    # render
    @classmethod
    def render(cls, elements: List, index: int) -> None:
        # draw main block
        renderer.draw_block(
            cls.block_menu.get_centered_x(), Constants.OFFSET_MENU_Y,
            cls.block_menu, 'white', 3)

        # draw items
        for i, a in enumerate(cls.anchors):
            offset: Position = a
            item_name: str = elements[i] if i < len(elements) else '-'

            renderer.draw_text(
                cls.block_menu.get_centered_x() + offset.x,
                Constants.OFFSET_MENU_Y + offset.y,
                item_name, 'white', 3)

        # draw selection block
        offset: Position = cls.anchors[index]
        item_name: str = elements[index]
        block_select: GraphicBlock = GraphicBlock.make_box(len(item_name), 1)

        renderer.draw_block(
            cls.block_menu.get_centered_x() + offset.x - 1,
            Constants.OFFSET_MENU_Y + offset.y - 1,
            block_select, 'white', 3)


class TextDisplay:
    block: GraphicBlock = GraphicBlock(Constants.GRAPHIC_MENU)
    anchor = Constants.MENU_ANCHORS[0]

    texts: List[str] = []
    text_current: Optional[str] = None
    chars_remaining: int = 0
    done: bool = True

    # state
    @classmethod
    def add_texts(cls, texts: List[str]) -> None:
        for t in texts:
            text: str = cls.get_formatted_text(t)
            cls.texts.append(text)

        cls.text_current = cls.texts.pop(0)
        cls.chars_remaining = len(cls.text_current)
        cls.done = False

    @classmethod
    def update_text(cls) -> None:
        if cls.chars_remaining > 0:
            cls.chars_remaining = 0
            return

        if len(cls.texts) > 0:
            cls.text_current = cls.texts.pop(0)
            cls.chars_remaining = len(cls.text_current)
            return

        cls.done = True

    # helper
    @classmethod
    def get_formatted_text(cls, text: str) -> str:
        words: List[str] = text.split(' ')
        text_new: str = words.pop(0)
        length: int = len(text_new)
        wrapped: bool = False

        for w in words:
            if length + len(w) + 1 <= Constants.LENGTH_TEXT:
                text_new += f' {w}'
                length += len(w) + 1
            else:
                if wrapped:
                    assert False  # text too long; straight to the shadow realm

                text_new += f'\n\n{w}'
                length = len(w)
                wrapped = True
        return text_new

    # render
    @classmethod
    def render(cls) -> None:
        # draw block
        renderer.draw_block(
            cls.block.get_centered_x(), Constants.OFFSET_MENU_Y,
            cls.block, 'white', 3)

        # draw text
        len_string: int = len(cls.text_current) - cls.chars_remaining

        renderer.draw_text(
            cls.block.get_centered_x() + cls.anchor.x,
            Constants.OFFSET_MENU_Y + cls.anchor.y,
            cls.text_current[:len_string], 'white', 3)

        # update characters
        if cls.chars_remaining > 0:
            cls.chars_remaining -= 1


class Field:
    MOVE_DELAY: int = 2
    PAD_INFO_AND_FIELD = 8

    block_field: GraphicBlock = GraphicBlock(Constants.GRAPHIC_BATTLE)
    block_select: GraphicBlock = GraphicBlock(
        Constants.GRAPHIC_SELECT_POSITION)

    positions: List[BattlePosition] = [
        BattlePosition(1, 1),
        BattlePosition(1, 3),
        BattlePosition(1, 5),
        BattlePosition(1, 7),
        BattlePosition(9, 1),
        BattlePosition(9, 3),
        BattlePosition(9, 5),
        BattlePosition(9, 7)]

    position_middle: BattlePosition = BattlePosition(5, 4)

    # state
    @classmethod
    def add_units(cls, party: List[Unit], enemies: List[Unit]) -> None:
        for u in party:
            cls.positions[cls.get_empty_index(Teams.PLAYER)].unit = u
        for u in enemies:
            cls.positions[cls.get_empty_index(Teams.ENEMY)].unit = u

    @classmethod
    def do_attack(cls, attacker: Unit, attack_index: int, target_index: int)\
            -> str:
        attack: Attack = attacker.attacks[attack_index]
        defender: Unit = cls.positions[target_index].unit

        defender.hp -= attack.attack_type.damage

        return f'{attacker.unit_type.name} attacks ' \
               f'{defender.unit_type.name} with {attack.attack_type.name}!'

    # helper
    # todo: this looks awful but isn't necessarily bad
    @classmethod
    def change_target(cls, index: int, key: int) -> int:
        if key == TK_UP:
            for i in range(index - 1, -1, -1):
                if cls.positions[i].unit:
                    return i

        if key == TK_DOWN:
            for i in range(index + 1, Constants.SIZE_SIDES):
                if cls.positions[i].unit:
                    return i

        return index

    @classmethod
    def get_team_bounds(cls, team: Teams) -> (int, int):
        if not team:
            return 0, Constants.SIZE_SIDES * 2

        if team == Teams.ENEMY:
            return 0, Constants.SIZE_SIDES

        if team == Teams.PLAYER:
            return Constants.SIZE_SIDES, Constants.SIZE_SIDES * 2

    @classmethod
    def get_index(
            cls, key: Callable[[Unit], bool], team: Optional[Teams]) -> int:
        bounds = cls.get_team_bounds(team)
        for i, p in enumerate(cls.positions[bounds[0]:bounds[1]]):
            if p.unit and key(p.unit):
                return bounds[0] + i

        return -1

    # there's a way to combine this, but ehhhh
    @classmethod
    def get_empty_index(cls, team: Optional[Teams]) -> int:
        bounds = cls.get_team_bounds(team)
        for i, p in enumerate(cls.positions[bounds[0]:bounds[1]]):
            if not p.unit:
                return bounds[0] + i

        return -1

    # currently a misnomer
    @classmethod
    def get_closest_target(cls) -> int:
        for i, p in enumerate(cls.positions[:Constants.SIZE_SIDES]):
            if p.unit:
                return i
        assert False

    # i guess this is fine
    @classmethod
    def get_units_by_team(cls, team: Teams) -> List[Unit]:
        return [p.unit for p in cls.positions
                if p.unit and p.unit.unit_type.team == team]

    # render
    @classmethod
    def render(cls, unit_center: Optional[Unit]) -> None:
        # draw field
        renderer.draw_block(
            cls.block_field.get_centered_x(), cls.block_field.get_centered_y(),
            cls.block_field, Constants.COLOR_FIELD, 1)

        # draw units
        for p in cls.positions:
            if not p.unit or p.unit is unit_center:
                continue

            renderer.draw_unit(
                cls.block_field.get_centered_x() + p.x,
                cls.block_field.get_centered_y() + p.y,
                p.unit, 2)

        # draw center unit
        if unit_center:
            renderer.draw_unit(
                cls.block_field.get_centered_x() + cls.position_middle.x,
                cls.block_field.get_centered_y() + cls.position_middle.y,
                unit_center, 2)

        # draw info blocks
        # todo: fung shei this
        enemies: List[Unit] = cls.get_units_by_team(Teams.ENEMY)
        if enemies:
            cls.draw_info_block(
                enemies,
                lambda b: cls.block_field.get_centered_x()
                          - b.width
                          - cls.PAD_INFO_AND_FIELD)

        party: List[Unit] = cls.get_units_by_team(Teams.PLAYER)
        if party:
            cls.draw_info_block(
                party,
                lambda b: cls.block_field.get_centered_x()
                          + cls.block_field.width
                          + cls.PAD_INFO_AND_FIELD)

    # todo: also extract these lol
    @classmethod
    def make_info_block(cls, units: List[Unit]) -> GraphicBlock:
        # calculate width
        max_name_length: int = max(len(u.unit_type.name) for u in units)
        max_hp = max(u.unit_type.hp_base for u in units)
        max_hp_string_length: int = len(f'{max_hp}/{max_hp}')
        length_max_string: int = max(max_name_length, max_hp_string_length) + 1

        return GraphicBlock.make_box(length_max_string, len(units) * 3 - 1)

    @classmethod
    def draw_info_block(
            cls, units: List[Unit], get_length: Callable[[GraphicBlock], int])\
            -> None:
        block: GraphicBlock = cls.make_info_block(units)
        anchor: Position = Position(get_length(block), block.get_centered_y())

        renderer.draw_block(anchor.x, anchor.y, block, 'white', 3)

        # draw unit info
        for i, u in enumerate(units):
            hp_string: str = f'{u.hp}/{u.unit_type.hp_base}'

            renderer.draw_text(
                anchor.x + 1, anchor.y + i * 3 + 1,
                u.unit_type.name, u.unit_type.color, 3)
            renderer.draw_text(
                anchor.x + block.width - len(hp_string) - 1,
                anchor.y + i * 3 + 2,
                hp_string, 'white', 3)

    @classmethod
    def draw_selected_target(cls, position_selected: int) -> None:
        position: BattlePosition = cls.positions[position_selected]

        x: int = cls.block_field.get_centered_x() + position.x
        y: int = cls.block_field.get_centered_y() + position.y

        renderer.draw_block(
            x - 1, y - 1, cls.block_select, Constants.COLOR_SELECT, 4)


class Timeline:
    # 0 1 2 3 4 5 6 7 8 9 10
    # ├─────────────────────┤

    block: GraphicBlock = GraphicBlock(Constants.GRAPHIC_TIMELINE)

    # this isn't a true BattlePosition, but it works
    points: List[TimelinePoint] = [
        TimelinePoint(0),
        TimelinePoint(2),
        TimelinePoint(4),
        TimelinePoint(6),
        TimelinePoint(8),
        TimelinePoint(10),
        TimelinePoint(12),
        TimelinePoint(14),
        TimelinePoint(16),
        TimelinePoint(18),
        TimelinePoint(20)]

    battle_units: List[Unit] = []
    current_unit: Optional[Unit] = None

    # state
    @classmethod
    def add_units(cls, party: List[Unit], enemies: List[Unit]) -> None:
        for u in party:
            u.battle_delay = 10 - u.speed
        for u in enemies:
            u.battle_delay = 10 - u.speed

        for u in party:
            cls.battle_units.append(u)
        for u in enemies:
            cls.battle_units.append(u)

        cls.sort_units()

        while cls.battle_units[0].battle_delay > 0:
            cls.update_tick()

    @classmethod
    def sort_units(cls) -> None:
        cls.battle_units.sort(key=lambda u: u.battle_delay)

    # todo: also fung shei this lol
    @classmethod
    def update_points(cls, projected_delay: int) -> None:
        # if there's no projected delay, just place in order
        # otherwise, hold the current unit, place remaining units, then current

        for p in cls.points:
            p.units = []

        if projected_delay:
            for u in cls.battle_units:
                if u is not cls.current_unit:
                    cls.points[u.battle_delay].units.append(u)
            cls.points[projected_delay].units.append(cls.current_unit)
        else:
            for u in cls.battle_units:
                cls.points[u.battle_delay].units.append(u)

    @classmethod
    def apply_delay(cls, index_attack: int) -> None:
        unit: Unit = cls.battle_units.pop(0)
        delay: int = unit.attacks[index_attack].attack_type.delay
        unit.battle_delay = delay

        count = 0

        for u in cls.battle_units:
            if delay < u.battle_delay:
                break
            count += 1

        cls.battle_units.insert(count, unit)

    @classmethod
    def update_tick(cls) -> None:
        for u in cls.battle_units:
            u.battle_delay -= 1

    # helper
    # i bet i could extend List to make anything like this searchable lol
    @classmethod
    def get_index(cls, key: Callable[[Unit], bool]) -> int:
        for i, u in enumerate(cls.battle_units):
            if key(u):
                return i

    @classmethod
    def get_unit(cls, key: Callable[[Unit], bool]) -> Unit:
        for u in cls.battle_units:
            if key(u):
                return u

    # render
    @classmethod
    def render(cls, delay_projected: int) -> None:
        # draw timeline
        renderer.draw_block(
            cls.block.get_centered_x(), Constants.OFFSET_TIMELINE_Y,
            cls.block, 'white', 3)

        cls.update_points(delay_projected)

        # draw units by cycling through timeline points
        for i, p in enumerate(cls.points):
            for j, u in enumerate(p.units):
                renderer.draw_unit(
                    cls.block.get_centered_x() + p.x,
                    Constants.OFFSET_TIMELINE_Y + 3 + j,
                    u, 3)
