from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Local helper – request/response models and normalization helpers for OCR & layout extraction


class FieldModel(BaseModel):
    type: str = Field(..., description="Field type, e.g., 'key_value', 'line'")
    key: Optional[Dict[str, Any]] = Field(None, description="Key object for key_value")
    value: Optional[Dict[str, Any]] = Field(
        None, description="Value object for key_value"
    )
    confidence: Optional[float] = None

    class Config:
        arbitrary_types_allowed = True


class LineModel(BaseModel):
    text: str = Field(..., description="Extracted line text")
    confidence: Optional[float] = None
    # Additional fields can be added as needed


class BlockModel(BaseModel):
    block_type: str = Field(..., description="Block type (paragraph, title, etc.)")
    text: str = Field(..., description="Full text of the block")
    confidence: Optional[float] = None
    # Optional nested structure like lines, words etc.


class PageModel(BaseModel):
    lines: List[LineModel] = Field(
        default_factory=list, description="List of extracted lines"
    )
    blocks: List[BlockModel] = Field(
        default_factory=list, description="List of detected blocks"
    )
    tables: List[Any] = Field(
        default_factory=list, description="Raw table structures returned by provider"
    )
    fields: List[FieldModel] = Field(
        default_factory=list, description="Extracted key-value or other fields"
    )


class LayoutResultModel(BaseModel):
    pages: List[PageModel] = Field(default_factory=list, description="Layout per page")
    confidence: Optional[float] = None


class DocumentResultModel(BaseModel):
    text: str = Field(..., description="Raw extracted plain text")
    layout: LayoutResultModel = Field(..., description="Structured layout information")


def normalize_response(raw: Dict[str, Any]) -> DocumentResultModel:
    """Convert provider-specific raw response into a unified model."""
    layout = LayoutResultModel(
        pages=[
            PageModel(
                lines=[LineModel(text=l["text"]) for l in raw.get("lines", [])],
                blocks=[
                    BlockModel(block_type=blk["type"], text=blk["text"])
                    for blk in raw.get("blocks", [])
                ],
                tables=raw.get("tables", []),  # keep raw for later processing
                fields=[FieldModel(**f) for f in (raw.get("fields") or [])],
            )
        ]
    )
    text = ". ".join(line["text"] for line in raw.get("lines", []))
    return DocumentResultModel(text=text, layout=layout)


# Example minimal usage / test
if __name__ == "__main__":
    mock_raw = {
        "text": "Demo text",
        "lines": [{"text": "Line 1"}, {"text": "Line 2"}],
        "blocks": [{"type": "paragraph", "text": "Paragraph block"}],
        "tables": [[{"rows": [[{"text": "Cell 1"}, {"text": "Cell 2"}]]}]],
        "fields": [
            {"type": "key_value", "key": {"text": "Name"}, "value": {"text": "John"}}
        ],
    }
    normalized = normalize_response(mock_raw)
    print(normalized.json(indent=2))
