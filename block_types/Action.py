from dataclasses import dataclass
from typing import Self

from block_types.Value import Value, get_str_repr_of_builtin
from util import Meta, RAW, CheckStatus
from block_types.Block import Block


@dataclass
class Action(Block):
    #| -1, type, None, uuid, false, ~[value]

    type_: int
    index_: int
    args: list[Value]
    _raw: RAW
    _meta: Meta

    @classmethod
    def _parse(cls, raw: RAW, meta: Meta) -> Self:
        type_ = raw[1]
        index_ = raw[0]
        raw_args = raw[5] if len(raw) == 6 else []
        args = [Value.parse(raw_arg, meta) for raw_arg in raw_args]

        return cls(type_, index_, args, raw, meta)
    
    @staticmethod
    def check(raw: RAW, meta: Meta) -> CheckStatus:
        if (len(raw) not in {5, 6} or
            type(raw[0]) is not int or
            type(raw[1]) is not int or
            (len(raw) == 6 and type(raw[5]) is not list)):

            return CheckStatus.Error
        return CheckStatus.Ok
    
    def __str__(self):
        return get_str_repr_of_builtin(self.type_, self.index_, self.args, self.meta)

    def __repr__(self):
        return super().__repr__()
