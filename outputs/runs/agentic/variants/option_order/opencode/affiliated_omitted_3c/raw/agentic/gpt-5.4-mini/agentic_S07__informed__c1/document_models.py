from dataclasses import dataclass
from typing import Any, Dict, List


def _blocks(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return response.get("Blocks", []) if isinstance(response, dict) else []


def normalize_text(response: Dict[str, Any]) -> str:
    parts = []
    for block in _blocks(response):
        if block.get("BlockType") == "LINE" and block.get("Text"):
            parts.append(block["Text"])
    return "
".join(parts)


def normalize_blocks(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _blocks(response)


def normalize_tables(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [b for b in _blocks(response) if b.get("BlockType") == "TABLE"]


def normalize_key_values(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [b for b in _blocks(response) if b.get("BlockType") in {"KEY_VALUE_SET", "WORD", "LINE"}]


@dataclass
class OCRRequest:
    bucket: str = None
    key: str = None
    bytes_data: bytes = None


@dataclass
class OCRResponse:
    raw: Dict[str, Any]
    text: str


@dataclass
class LayoutResponse:
    raw: Dict[str, Any]
    blocks: List[Dict[str, Any]]


@dataclass
class TableResponse:
    raw: Dict[str, Any]
    tables: List[Dict[str, Any]]


@dataclass
class KeyValueResponse:
    raw: Dict[str, Any]
    key_values: List[Dict[str, Any]]
