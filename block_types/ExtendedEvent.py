from dataclasses import dataclass
from typing import Self

from util import META, RAW, CheckStatus
from block_types.Event import Event
from block_types.Condition import Condition
from block_types.Action import Action
from block_types.Code import Code


@dataclass
class ExtendedEvent(Event):
    #| 0, None, false, None, uuid, [condition], [action], [code]

    conditions: list[Condition]
    actions: list[Action]
    code: list[Code] = None
    _raw: RAW
    _meta: META

    @classmethod
    def _parse(cls, raw, meta) -> Self:
        self = super()._parse(raw, meta)
        raw_code = raw[7]
        self.code = [Code.parse(i, meta) for i in raw_code]
        return self

    @staticmethod
    def check(raw: RAW, meta: META) -> CheckStatus:
        if (len(raw) != 8 or
            type(raw[5]) is not list or
            type(raw[6]) is not list or
            type(raw[7]) is not list):

            return CheckStatus.Error
        return CheckStatus.Ok

    def __str__(self):
        return self.collapse()

    def collapse(self, depth=0) -> str:
        output = super().collapse(depth)
        str_code = [i.collapse(depth + 1) for i in self.code]

        if str_code:
            return output + "".join(str_code)

        return output
