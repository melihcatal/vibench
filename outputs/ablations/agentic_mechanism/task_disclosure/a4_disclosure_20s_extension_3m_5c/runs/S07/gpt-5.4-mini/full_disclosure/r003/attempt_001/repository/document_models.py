from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(frozen=True)
class OCRRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    language_hints: Sequence[str] = field(default_factory=tuple)
    mime_type: str = "image/png"

    def resolve_image_bytes(self) -> bytes:
        if self.image_bytes is not None:
            return self.image_bytes
        if not self.image_path:
            raise ValueError("image_path or image_bytes is required")
        with open(self.image_path, "rb") as f:
            return f.read()

    def to_payload(self) -> Dict[str, Any]:
        image_bytes = self.resolve_image_bytes()
        payload: Dict[str, Any] = {
            "requests": [
                {
                    "image": {"content": base64.b64encode(image_bytes).decode("utf-8")},
                    "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
                }
            ]
        }
        if self.language_hints:
            payload["requests"][0]["imageContext"] = {"languageHints": list(self.language_hints)}
        return payload


@dataclass(frozen=True)
class LayoutRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mode: str = "DOCUMENT_TEXT_DETECTION"
    mime_type: str = "image/png"

    def resolve_image_bytes(self) -> bytes:
        if self.image_bytes is not None:
            return self.image_bytes
        if not self.image_path:
            raise ValueError("image_path or image_bytes is required")
        with open(self.image_path, "rb") as f:
            return f.read()

    def to_payload(self) -> Dict[str, Any]:
        image_bytes = self.resolve_image_bytes()
        return {
            "requests": [
                {
                    "image": {"content": base64.b64encode(image_bytes).decode("utf-8")},
                    "features": [{"type": self.mode}],
                }
            ]
        }


@dataclass(frozen=True)
class NormalizedWord:
    text: str
    confidence: Optional[float] = None
    bounding_box: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class NormalizedLine:
    text: str
    words: Sequence[NormalizedWord] = field(default_factory=tuple)
    confidence: Optional[float] = None
    bounding_box: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class NormalizedBlock:
    block_type: str
    lines: Sequence[NormalizedLine] = field(default_factory=tuple)
    confidence: Optional[float] = None
    bounding_box: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class OCRResponse:
    text: str
    raw: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LayoutResponse:
    blocks: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    lines: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    tables: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    raw: Mapping[str, Any] = field(default_factory=dict)


def normalize_ocr_response(data: Mapping[str, Any]) -> OCRResponse:
    responses = data.get("responses", []) if isinstance(data, Mapping) else []
    if not responses:
        return OCRResponse(text="", raw=data)
    response = responses[0]
    text = response.get("fullTextAnnotation", {}).get("text") or ""
    if not text:
        annotations = response.get("textAnnotations", [])
        if annotations:
            text = annotations[0].get("description", "") or ""
    return OCRResponse(text=text, raw=response)


def normalize_layout_response(data: Mapping[str, Any]) -> LayoutResponse:
    responses = data.get("responses", []) if isinstance(data, Mapping) else []
    if not responses:
        return LayoutResponse(raw=data)
    annotation = responses[0]
    pages = annotation.get("fullTextAnnotation", {}).get("pages", [])
    blocks: List[Mapping[str, Any]] = []
    lines: List[Mapping[str, Any]] = []
    tables: List[Mapping[str, Any]] = []
    for page in pages:
        for block in page.get("blocks", []):
            blocks.append(block)
            if block.get("blockType") == "TABLE":
                tables.append(block)
            for paragraph in block.get("paragraphs", []):
                for word in paragraph.get("words", []):
                    symbols = word.get("symbols", [])
                    lines.append(
                        {
                            "text": "".join(symbol.get("text", "") for symbol in symbols),
                            "confidence": word.get("confidence"),
                            "boundingBox": word.get("boundingBox"),
                        }
                    )
    return LayoutResponse(blocks=tuple(blocks), lines=tuple(lines), tables=tuple(tables), raw=annotation)
