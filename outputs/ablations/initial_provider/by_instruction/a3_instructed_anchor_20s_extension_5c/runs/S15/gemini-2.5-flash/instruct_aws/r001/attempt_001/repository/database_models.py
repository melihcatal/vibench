import typing

class Document(typing.TypedDict):
    id: str
    content: typing.Dict[str, typing.Any]

class Record(typing.TypedDict):
    id: str
    summary: typing.Optional[str]
    safe_content: typing.Optional[bool]
    translated_content: typing.Optional[typing.Dict[str, str]]
