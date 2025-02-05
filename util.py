from enum import Enum, auto
import json


META = tuple[str, ...]
RAW_VALUE = str | float | int | None
RAW = list[RAW_VALUE]


def extract_meta(c2runtime_path: str) -> META:
    line_start = "cr.getObjectRefTable = function () { return [\n"
    line_end = "];};\n"

    with open(c2runtime_path, "r", encoding="utf-8-sig") as f:
        output: list[str] = []
        start_output = False
        for line in f.readlines():
            if not start_output:
                if line == line_start:
                    start_output = True
                continue

            if line == line_end:
                return tuple(output)
            
            output.append(extract_transistor_name(line))

    raise ValueError("Could not find proper EOF for meta")


def extract_transistor_name(line: str) -> str:
    transistor_name = line.split(".")[-1].replace(",", "")[:-1]

    if line.count(".") <= 2:
        return transistor_name
    
    transistor_parent_name = line.split(".")[-4]
    return f"{transistor_parent_name}.{transistor_name}"


def get_data(data_path: str):
    with open(data_path, "r", encoding="utf-8-sig") as data_f:
        data = json.load(data_f)["project"][6][0][1]

    return data


def save_decoded(decoded: str, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(decoded)


class CheckStatus(Enum):
    Ok = auto()
    Error = auto()


class ParseError(ValueError):
    def __init__(self, raw: RAW) -> None:
        super().__init__(f"Can't parse raw: {raw}")
