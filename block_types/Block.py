from copy import copy
from typing import Self
from abc import ABC, abstractmethod

from util import RAW, CheckStatus, ParseError, Meta


class Block(ABC):
    _raw: RAW
    _meta: Meta

    @property
    def raw(self):
        return copy(self._raw)

    @property
    def meta(self):
        return self._meta

    @classmethod
    def parse(cls, raw: RAW, meta: Meta) -> Self:
        match cls.check(raw, meta):
            case CheckStatus.Ok:
                return cls._parse(raw, meta)
            case CheckStatus.Error:
                raise ParseError(raw)

    @classmethod
    @abstractmethod
    def _parse(cls, raw: RAW, meta: Meta) -> Self:
        ...
    
    @staticmethod
    @abstractmethod
    def check(raw: RAW, meta: Meta) -> CheckStatus:
        ...

    def __repr__(self):
        out = "<" + self.__str__().replace("\n", "\\n") + ">"
        while "  " in out:
            out = out.replace("  ", " ")
        return out