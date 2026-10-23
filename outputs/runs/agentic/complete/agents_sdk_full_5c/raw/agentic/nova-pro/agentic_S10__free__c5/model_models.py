from dataclasses import dataclass

@dataclass
class Request:
    task: str
    model: str
    input_text: str

@dataclass
class Response:
    output_text: str