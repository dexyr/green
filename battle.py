# this module just maps the logic for states without needing to include it at
#   the bottom of battle_states

from typing import List

from bearlibterminal import terminal

from data import Unit

from battle_states import BattleState, Start
from battle_util import Timeline


class Battle:
    state: BattleState = Start

    @classmethod
    def logic(cls):
        if state_new := cls.state.logic():  # neat
            cls.state = state_new

    @classmethod
    def render(cls):
        cls.state.render()
        print_debug()


def print_debug() -> None:
    terminal.layer(10)
    terminal.color(terminal.color_from_name('white'))

    units: List[Unit] = Timeline.battle_units

    terminal.printf(0, 0, f'state: {Battle.state}')
    # terminal.printf(0, 1, f'sub-state: {BattleScript.sub_state}')

    for i, u in enumerate(units):
        unit = u
        terminal.printf(
            0, 3 + i, f'{unit.unit_type.name}, delay: {unit.battle_delay}')
