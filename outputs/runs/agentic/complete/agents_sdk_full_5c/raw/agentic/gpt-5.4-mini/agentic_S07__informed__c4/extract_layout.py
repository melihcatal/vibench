from __future__ import annotations

from typing import List

from document_client import DocumentAIClientHelper
from document_models import DocumentRequest, LayoutBlock, normalize_text


def extract_layout(file_path: str, mime_type: str = "image/png") -> List[LayoutBlock]:
    helper = DocumentAIClientHelper()
    response = helper.process(DocumentRequest(file_path=file_path, mime_type=mime_type))
    document = response.document
    blocks: List[LayoutBlock] = []
    for page in getattr(document, "pages", []):
        for paragraph in getattr(page, "paragraphs", []):
            blocks.append(LayoutBlock(kind="paragraph", text=normalize_text(getattr(paragraph, "layout", {}).get("text_anchor", {})), raw=paragraph))
        for block in getattr(page, "blocks", []):
            blocks.append(LayoutBlock(kind="block", text=normalize_text(getattr(block, "layout", {}).get("text_anchor", {})), raw=block))
    return blocks
