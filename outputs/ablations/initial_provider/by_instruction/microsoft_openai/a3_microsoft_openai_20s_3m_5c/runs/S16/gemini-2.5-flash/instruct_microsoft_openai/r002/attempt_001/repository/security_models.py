from dataclasses import dataclass

@dataclass
class Secret:
    name: str
    value: str
    content_type: str = "text/plain"
    tags: dict = None
