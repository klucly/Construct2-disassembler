from dataclasses import dataclass
from typing import Self

from util import Meta, RAW, CheckStatus
from block_types.Block import Block
from block_types.Code import Code


@dataclass
class Group(Block):
    #| 0, [true, name], false, None, uuid, [group_body], [], [code]

    name: str
    code: list[Code]
    _raw: RAW
    _meta: Meta

    @classmethod
    def _parse(cls, raw: RAW, meta: Meta) -> Self:
        name = raw[1][1]
        raw_code = raw[7]

        code = [Code.parse(raw_code_snippet, meta) for raw_code_snippet in raw_code]

        return cls(name, code, raw, meta)
    
    @staticmethod
    def check(raw: RAW, meta: Meta) -> CheckStatus:
        if (len(raw) != 8 or
            type(raw[1]) is not list or
            len(raw[1]) != 2 or
            type(raw[1][1]) is not str or
            type(raw[5]) is not list or
            type(raw[7]) is not list):

            return CheckStatus.Error
        return CheckStatus.Ok

    def __str__(self):
        return self.collapse()

    def collapse(self, depth=0) -> str:
        output_start = "    "*depth + f"Group {self.name}:\n"

        str_code = [i.collapse(depth + 1) for i in self.code]

        if str_code:
            return output_start + "".join(str_code)

        return output_start + " pass\n"
