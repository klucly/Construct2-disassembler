from typing import Self

from block_types.Block import Block
from block_types.Value import Value
from block_types.Condition import Condition
from block_types.Action import Action
from block_types.Event import Event
from block_types.DefVariable import DefVariable
from block_types.Group import Group
from block_types.Code import Code
from block_types.ExtendedEvent import ExtendedEvent
from util import RAW, CheckStatus, Meta


class _Block:
    @classmethod
    def _parse(cls, raw: RAW, meta: Meta) -> Self:
        if Value.check(raw, meta) == CheckStatus.Ok:
            return Value.parse(raw, meta)
        if Code.check(raw, meta) == CheckStatus.Ok:
            return Code.parse(raw, meta)
        if Condition.check(raw, meta) == CheckStatus.Ok:
            return Condition.parse(raw, meta)
        if Action.check(raw, meta) == CheckStatus.Ok:
            return Action.parse(raw, meta)

    @staticmethod
    def check(raw: RAW, meta: Meta) -> CheckStatus:
        if (Value.check(raw, meta) == CheckStatus.Error and
            Code.check(raw, meta) == CheckStatus.Error and
            Condition.check(raw, meta) == CheckStatus.Error and
            Action.check(raw, meta) == CheckStatus.Error):
            
            return CheckStatus.Error
        return CheckStatus.Ok

Block._parse = _Block._parse
Block.check = _Block.check


class _Code:
    @classmethod
    def _parse(cls, raw: RAW, meta: Meta) -> Self:
        if DefVariable.check(raw, meta) == CheckStatus.Ok:
            return DefVariable.parse(raw, meta)
        if Event.check(raw, meta) == CheckStatus.Ok:
            return Event.parse(raw, meta)
        if Group.check(raw, meta) == CheckStatus.Ok:
            return Group.parse(raw, meta)
        if ExtendedEvent.check(raw, meta) == CheckStatus.Ok:
            return ExtendedEvent.parse(raw, meta)
    
    @staticmethod
    def check(raw: RAW, meta: Meta) -> CheckStatus:
        if (DefVariable.check(raw, meta) == CheckStatus.Error and
            Event.check(raw, meta) == CheckStatus.Error and
            Group.check(raw, meta) == CheckStatus.Error and
            ExtendedEvent.check(raw, meta) == CheckStatus.Error):
            
            return CheckStatus.Error
        return CheckStatus.Ok

Code._parse = _Code._parse
Code.check = _Code.check

