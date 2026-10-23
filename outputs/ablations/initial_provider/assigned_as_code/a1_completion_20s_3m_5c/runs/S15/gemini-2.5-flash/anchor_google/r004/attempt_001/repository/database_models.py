import dataclasses
import typing

@dataclasses.dataclass
class Document:
    id: str
    data: typing.Dict

@dataclasses.dataclass
class QueryCondition:
    field: str
    operator: str  # e.g., '==', '>', '<'
    value: typing.Any
