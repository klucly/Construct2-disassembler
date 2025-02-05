from dataclasses import dataclass
from typing import Any, Self

from util import RAW, RAW_VALUE, META, CheckStatus, ParseError
from block_types.Block import Block


class Value(Block):
    #| RAW_VALUE
    #| [Value]
    #| type, Value
    #| type, [Value]
    #| int, type, [Value]
    #| type, [Value], [Value]
    #| callee, int, bool, None, int
    #| type, int, callee, bool, None
    #| type, int, callee, bool, None, [Value]
    
    @classmethod
    def _parse(cls, raw: RAW, meta: META) -> Self:
        if ContainerValue.check(raw, meta) == CheckStatus.Ok:
            return ContainerValue.parse(raw, meta)
        if SimpleValue.check(raw, meta) == CheckStatus.Ok:
            return SimpleValue.parse(raw, meta)
        if CallValue.check(raw, meta) == CheckStatus.Ok:
            return CallValue.parse(raw, meta)
        if OperatorValue.check(raw, meta) == CheckStatus.Ok:
            return OperatorValue.parse(raw, meta)
        
        raise ParseError(raw)
        
    @staticmethod
    def check(raw: RAW, meta: META) -> CheckStatus:
        if (SimpleValue.check(raw, meta) == CheckStatus.Error and
            CallValue.check(raw, meta) == CheckStatus.Error and
            OperatorValue.check(raw, meta) == CheckStatus.Error and
            ContainerValue.check(raw, meta) == CheckStatus.Error):

            return CheckStatus.Error
        return CheckStatus.Ok


@dataclass
class ContainerValue(Value):
    values: list[Value]
    _raw: RAW
    _meta: META

    @classmethod
    def _parse(cls, raw: RAW, meta: META) -> Self:
        values = [Value.parse(i, meta) for i in raw]
        return cls(values, raw, meta)
        
    @staticmethod
    def check(raw: RAW, meta: META) -> CheckStatus:
        if type(raw) is list and min([type(i) is list for i in raw]) == 1:
            return CheckStatus.Ok
        return CheckStatus.Error
    
    def __str__(self):
        str_values = [str(value) for value in self.values]
        return ", ".join(str_values)

@dataclass
class SimpleValue(Value):
    #| RAW_VALUE
    #| [Value]
    #| type, Value
    #| type, [Value]

    type_: int
    value: RAW_VALUE
    _raw: RAW
    _meta: META

    @classmethod
    def _parse(cls, raw: RAW, meta: META) -> Self:
        if type(raw) is not list:
            return cls([int, float, str].index(type(raw)), raw, raw, meta)
        
        if len(raw) == 1:
            return Value.parse(raw[0], meta)
        if len(raw) == 2:
            if type(raw[1]) is list:
                return Value.parse(raw[1], meta)
                
            else:
                return cls(raw[0], raw[1], raw, meta)
        
        raise ValueError("Unhandled case. check may be wrong")

    @staticmethod
    def decode_value_type(type_index: int | str, value: Any) -> Any:
        if type(type_index) is str and not value:
            return type_index

        match type_index:
            # int
            case 0:
                return value
            # float
            case 1:
                return value
            # string
            case 2:
                return value
            # choice
            case 3:
                return f"#{value}"
            # object
            case 4:
                return f"@{value}"
            # cmp sign
            case 8:
                return [
                    "=",
                    "!=",
                    "<",
                    "<=",
                    ">",
                    ">=",
                ][value]
            # Choice with none or special keys on keyboard (not clear)
            case 9:
                return value
            # instance variable
            case 10:
                return f"${value}"
            # variable
            case 11:
                return value
            # variable
            case 23:
                return value
            case a:
                return f"!ERROR-{a}!"
            
        # return {
        #     0: "int",
        #     1: "float",
        #     2: "string",
        #     3: "type|platform",
        #     5: "layer",
        #     7: "any",
        #     8: "cmp",
        #     11: "var"
        # }[i]

    @staticmethod
    def check(raw: RAW, meta: META) -> CheckStatus:
        if type(raw) is list and len(raw) not in {1, 2}:

            return CheckStatus.Error
        return CheckStatus.Ok
    
    def __str__(self):
        if type(self.value) is str and self.type_ == 2:
            return f'"{self.value}"'
        return str(self.decode_value_type(self.type_, self.value))


@dataclass
class CallValue(Value):
    #| callee, int, bool, None, int
    #| type, int, callee, bool, None
    #| type, int, callee, bool, None, [Value]

    callee_index: int
    callee_args: list[Value]
    _raw: RAW
    _meta: META

    @classmethod
    def _parse(cls, raw: RAW, meta: META) -> Self | list[Self]:
        callee_index = raw[2] if type(raw[2]) is int else raw[0]
        callee_args = [
            Value.parse(raw_value, meta) for raw_value in raw[5]
        ] if len(raw) == 6 else []

        return cls(callee_index, callee_args, raw, meta)

    @staticmethod
    def check(raw: RAW, meta: META) -> CheckStatus:
        if (type(raw) is not list or
            len(raw) not in {5, 6} or
            type(raw[0]) is not int or
            type(raw[2]) not in {int, bool} or
            (len(raw) == 6 and type(raw[5]) is not list)):

            return CheckStatus.Error
        return CheckStatus.Ok

    def __str__(self):
        output = self.meta[self.callee_index]
        if self.callee_args:
            str_args = [str(i) for i in self.callee_args]
            output += f"({', '.join(str_args)})"
        return output

@dataclass
class OperatorValue(Value):
    #| int, type, [Value]
    #| type, [Value], [Value]

    type_: int
    args: list[Value]
    _raw: RAW
    _meta: META

    @classmethod
    def _parse(cls, raw: RAW, meta: META) -> Self:
        arg2 = Value.parse(raw[2], meta)
        type_ = raw[1]
        args = [arg2]

        if type(raw[1]) is list:
            type_ = raw[0]
            arg1 = Value.parse(raw[1], meta)
            args = [arg1, arg2]

        return cls(type_, args, raw, meta)


    @staticmethod
    def check(raw: RAW, meta: META) -> CheckStatus:
        if (type(raw) is not list or
            len(raw) != 3 or
            type(raw[2]) is not list or
            type(raw[0]) is not int or
            type(raw[1]) not in {list, int}):

            return CheckStatus.Error
        return CheckStatus.Ok

    def __str__(self):
        str_args = [str(i) for i in self.args]
        if len(str_args) == 1:
            return f"{self.meta[self.type_]}({str_args[0]})"
        
        signs = {
            4: "+",
            5: "-",
            6: "*",
            7: "/",
            8: "%",
            9: "^",
            10: "&",
            11: "|",

            14: "<",
            16: ">"
        }

        return "(" + f" {signs[self.type_]} ".join(str_args) + ")"
