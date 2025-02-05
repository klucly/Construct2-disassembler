from dataclasses import dataclass
from typing import Self

from block_types.Value import Value
from util import Meta, RAW, CheckStatus
from block_types.Code import Code


@dataclass
class DefVariable(Code):
    #| int, name, int, value, bool, bool, uuid, bool

    name: str
    value: Value
    _raw: RAW
    _meta: Meta

    @classmethod
    def _parse(cls, raw: RAW, meta: Meta) -> Self:
        return cls(str(raw[1]), Value.parse(raw[3], meta), raw, meta)
    
    @staticmethod
    def check(raw: RAW, meta: Meta) -> CheckStatus:
        if (len(raw) != 8 or
            type(raw[1]) is not str):

            return CheckStatus.Error
        return CheckStatus.Ok

    def collapse(self, depth=0):
        return "    "*depth + str(self)

    def __str__(self):
        return f"{self.name} = {self.value}\n"
    