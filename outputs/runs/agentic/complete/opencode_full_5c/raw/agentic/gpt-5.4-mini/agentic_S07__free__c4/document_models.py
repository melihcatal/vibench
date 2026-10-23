from dataclasses import dataclass


@dataclass
class DocumentRequest:
    image_path: str


@dataclass
class TextResponse:
    text: str


@dataclass
class LayoutResponse:
    blocks: list
    lines: list
    tables: list


@dataclass
class TableResponse:
    tables: list


@dataclass
class KeyValueResponse:
    pairs: dict


def response_text(result) -> str:
    return getattr(result, "text", "") or ""
