import typing

class LLMRequest:
    text: str
    context: typing.Optional[str] = None
    question: typing.Optional[str] = None
    json_schema: typing.Optional[typing.Dict] = None

class LLMResponse:
    content: str
