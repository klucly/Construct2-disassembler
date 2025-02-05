from util import RAW, META
from block_types import Code


class Parser:
    def __init__(self, meta: META):
        self.meta = meta

    def parse(self, raw: RAW) -> list[Code]:
        return [Code.parse(b, self.meta) for b in raw]
