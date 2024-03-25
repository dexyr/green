# +------------------------------------------------------------------------+
# | silly design patterns i will probably grow to regret lol:              |
# |                                                                        |
# |   * objects can only act on their own members, meaning that no objects |
# |       should hold any references to objects they do not directly 'own' |
# |                                                                        |
# |   * classes should only be turned into objects when there are multiple |
# |       of them in existence at the same time                            |
# |                                                                        |
# +------------------------------------------------------------------------+

import os
import time

from bearlibterminal import terminal

import data
from world import World
from battle import Battle
import renderer

# venv here should be a holdover for pycharm
FONT_PATH: str = os.path.join(os.getcwd(), 'CGA8x8thick.png')

# variables for debugging
data.Globals.state = data.GameStates.BATTLE  # hard-coded for now


def render() -> None:
    renderer.clear()

    if data.Globals.state == data.GameStates.WORLD:
        World.render()

    if data.Globals.state == data.GameStates.BATTLE:
        Battle.render()

    terminal.refresh()


def logic() -> None:
    if data.Globals.state == data.GameStates.WORLD:
        World.logic()

    if data.Globals.state == data.GameStates.BATTLE:
        Battle.logic()


def game() -> None:
    frame_time = 1000000000 / 20  # the denominator is desired fps

    time_current = time.time_ns()
    time_last_update = time_current
    frame_counter = 0

    terminal.open()
    terminal.set(f'window: title=green, size=80x60')
    terminal.set(f'font: {FONT_PATH}, size=8x8, codepage=437, resize=16x16')

    terminal.refresh()

    while True:
        time_current = time.time_ns()

        while terminal.has_input():
            data.Globals.keys.append(terminal.read())

        if terminal.TK_CLOSE in data.Globals.keys:
            break

        logic()
        data.Globals.keys.clear()

        if time_current - time_last_update > frame_time:
            frame_counter += 1
            render()
            time_last_update = time_current


if __name__ == '__main__':
    game()
