from dataclasses import dataclass
from typing import Self

from util import Meta, RAW, CheckStatus
from block_types.Block import Block
from block_types.Condition import Condition
from block_types.Action import Action


@dataclass
class Event(Block):
    #| 0, None, false, None, uuid, [condition], [action]

    conditions: list[Condition]
    actions: list[Action]
    _raw: RAW
    _meta: Meta

    @classmethod
    def _parse(cls, raw: RAW, meta: Meta) -> Self:
        raw_conditions = raw[5]
        raw_actions = raw[6]

        conditions = [Condition.parse(raw_arg, meta) for raw_arg in raw_conditions]
        actions = [Action.parse(raw_arg, meta) for raw_arg in raw_actions]

        return cls(conditions, actions, raw, meta)
    
    @staticmethod
    def check(raw: RAW, meta: Meta) -> CheckStatus:
        if (len(raw) != 7 or
            type(raw[5]) is not list or
            type(raw[6]) is not list):

            return CheckStatus.Error
        return CheckStatus.Ok

    def __str__(self):
        return self.collapse()

    def collapse(self, depth=0, more_code_expected_later: bool = False) -> str:
        output_start = "    "*depth

        more_code_expected_here = len(self.actions) > 0

        str_conditions = [str(i) for i in self.conditions]
        str_actions = [str(i) for i in self.actions]

        if not str_conditions and not str_actions:
            return ""

        if not str_conditions:
            output_with_conditions = output_start + "if True:"
        elif len(str_conditions) == 1 and str_conditions[0] == "system_object.Else()":
            output_with_conditions = output_start + "else:"
        elif str_conditions[0] == "system_object.Else()":
            output_with_conditions = output_start + "elif " + " and ".join(str_conditions[1:]) + ":"
        else:
            output_with_conditions = output_start + "if " + " and ".join(str_conditions) + ":"

        if not more_code_expected_here and not more_code_expected_later:
            return output_with_conditions + " pass\n"

        if more_code_expected_here:
            return output_with_conditions + "\n" + "    "*(depth+1) + ("\n"+"    "*(depth+1)).join(str_actions) + "\n"
        return output_with_conditions + "\n"

    def __repr__(self):
        return super().__repr__()
