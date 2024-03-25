from typing import List

from bearlibterminal import terminal

from data import Unit

# # hex block thing
# block: renderer.GraphicBlock = renderer.GraphicBlock(
#     [' / \\ / \\ / \\',
#      '│   │   │   │',
#      '│   │   │   │',
#      ' \\ / \\ / \\ / \\',
#      '  │   │   │   │',
#      '  │   │   │   │',
#      ' / \\ / \\ / \\ /',
#      '│   │   │   │',
#      '│   │   │   │',
#      ' \\ / \\ / \\ / \\',
#      '  │   │   │   │',
#      '  │   │   │   │',
#      '   \\ / \\ / \\ /'])

# terminal layers:
#   0 - bg
#   1 - field
#   2 - units
#   3 - ui
#   4 - ui 2
#   10 - debug


class Constants:
    TERMINAL_WIDTH: int = 80
    TERMINAL_HEIGHT: int = 60


class GraphicBlock:
    def __init__(self, graphic: List[str]):
        self.width: int = len(graphic[0])
        self.height: int = len(graphic)
        self.graphic: List[str] = graphic

    def get_centered_x(self) -> int:
        return Constants.TERMINAL_WIDTH // 2 - self.width // 2

    def get_centered_y(self) -> int:
        return Constants.TERMINAL_HEIGHT // 2 - self.height // 2

    @staticmethod
    def make_box(width: int, height: int):
        assert width > 0 and height > 0  # no funny business

        # there's a better way to do this; i can smell it
        block: List[str] = ['┌' + '─' * width + '┐']
        for _ in range(height):
            block.append('│' + ' ' * width + '│')
        block.append('└' + '─' * width + '┘')

        return GraphicBlock(block)


def draw_block(x: int, y: int, block: GraphicBlock, color: str, layer: int)\
        -> None:
    terminal.color(terminal.color_from_name(color))
    terminal.layer(layer)

    for r in range(len(block.graphic)):
        for c in range(len(block.graphic[r])):
            if block.graphic[r][c] != ' ':
                terminal.put(x + c, y + r, block.graphic[r][c])


def draw_unit(x: int, y: int, unit: Unit, layer: int) -> None:
    terminal.color(terminal.color_from_name(unit.unit_type.color))
    terminal.layer(layer)

    terminal.put(x, y, unit.unit_type.char)


def draw_char(x: int, y: int, char: str, color: str, layer: int) -> None:
    assert len(char) == 1

    terminal.color(terminal.color_from_name(color))
    terminal.layer(layer)

    terminal.put(x, y, char)


def draw_text(x: int, y: int, text: str, color: str, layer: int) -> None:
    terminal.color(terminal.color_from_name(color))
    terminal.layer(layer)

    terminal.printf(x, y, text)


def clear() -> None:
    # clear screen? there must be an api function for this
    terminal.clear()
