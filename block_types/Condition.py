from dataclasses import dataclass
from typing import Self

from block_types.Value import Value, get_str_repr_of_builtin
from util import META, RAW, CheckStatus
from block_types.Block import Block


@dataclass
class Condition(Block):
    #| -1, type, None, int?, bool?, false, false, uuid, false, ~[value]

    type_: int
    index_: int
    args: list[Value]
    _raw: RAW
    _meta: META

    @classmethod
    def _parse(cls, raw: RAW, meta: META) -> Self:
        type_ = raw[1]
        index_ = raw[0]
        raw_args = raw[9] if len(raw) == 10 else []
        args = [Value.parse(raw_arg, meta) for raw_arg in raw_args]

        return cls(type_, index_, args, raw, meta)
    
    @staticmethod
    def check(raw: RAW, meta: META) -> CheckStatus:
        if (len(raw) not in {9, 10} or
            type(raw[0]) is not int or
            type(raw[1]) is not int or
            (len(raw) == 10 and type(raw[9]) is not list)):

            return CheckStatus.Error
        return CheckStatus.Ok

    def __str__(self):
        return get_str_repr_of_builtin(self.type_, self.index_, self.args, self.meta)
