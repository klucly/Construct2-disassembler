from enum import Enum, auto
from dataclasses import dataclass
import json


# Meta = tuple[str, ...]
RAW_VALUE = str | float | int | None
RAW = list[RAW_VALUE]


@dataclass
class Meta:
    _obj_names: tuple[str, ...]
    _instance_to_obj: tuple[int, ...]

    def get_name_by_id(self, id_: int) -> str:
        return self._obj_names[id_]
    
    def get_obj_by_instance_id(self, id_: int) -> int:
        return self._instance_to_obj[id_]
    
    def get_obj_name_by_instance_id(self, id_: int) -> str:
        return self.get_name_by_id(self.get_obj_by_instance_id(id_))


def extract_meta(data_path: str, c2runtime_path: str):
    return Meta(
        extract_obj_names(c2runtime_path),
        extract_instances_data(data_path)
    )


def extract_obj_names(c2runtime_path: str) -> tuple[str, ...]:
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


def extract_instances_data(data_path: str) -> tuple[str, ...]:
    with open(data_path, "r", encoding="utf-8-sig") as f:
        raw_data = json.load(f)
    data = raw_data["project"][3]
    instance_to_obj_list = []
    for instance in data:
        instance_to_obj_list.append(instance[1])
    return instance_to_obj_list


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
