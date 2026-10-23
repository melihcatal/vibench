from dataclasses import dataclass
from typing import Any


@dataclass
class DocumentSource:
    image_bytes: bytes | None = None
    s3_bucket: str | None = None
    s3_key: str | None = None


def normalize_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{k.lower(): v for k, v in block.items()} for block in blocks]
