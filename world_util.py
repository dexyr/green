"""
world toybox
"""

from typing import List

from data import BlockType, Constants


class Map:
    blocks: List[List[BlockType]]

    # state
    def __init__(self, string_map: List[str]):
        self.blocks = [[] for _ in string_map]

        for i, s in enumerate(string_map):
            for c in s:
                block: BlockType = Constants.STRING_MAP_MAP[c]
                #                ^ this will actually just error if anything

                if not block:
                    continue

                self.blocks[i].append(block)
