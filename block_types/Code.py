from block_types.Block import Block


class Code(Block):
    def collapse(self, depth=0) -> str:
        ...
