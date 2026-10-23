from __future__ import annotations

from typing import List

from document_client import begin_analyze_document
from document_models import LayoutElement, normalize_lines


def extract_layout(document) -> List[LayoutElement]:
    poller = begin_analyze_document("prebuilt-layout", document, content_type="application/octet-stream")
    result = poller.result()
    elements: List[LayoutElement] = []

    for paragraph in getattr(result, "paragraphs", []) or []:
        elements.append(
            LayoutElement(
                kind=getattr(paragraph, "role", None) or "paragraph",
                content=getattr(paragraph, "content", "") or "",
                bounding_regions=[br.as_dict() if hasattr(br, "as_dict") else br for br in getattr(paragraph, "bounding_regions", []) or []],
                confidence=getattr(paragraph, "confidence", None),
            )
        )

    for table in getattr(result, "tables", []) or []:
        table_text = []
        for cell in getattr(table, "cells", []) or []:
            table_text.append(getattr(cell, "content", "") or "")
        elements.append(LayoutElement(kind="table", content="\n".join(x for x in table_text if x), bounding_regions=[br.as_dict() if hasattr(br, "as_dict") else br for br in getattr(table, "bounding_regions", []) or []]))

    if not elements:
        for line in normalize_lines(getattr(result, "pages", []) or []):
            elements.append(LayoutElement(kind="line", content=line))

    return elements
