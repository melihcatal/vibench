from __future__ import annotations

from typing import List

from document_client import get_client, normalize_source
from document_models import LayoutBlock


def extract_layout(source: str) -> List[LayoutBlock]:
    client = get_client()
    payload = normalize_source(source)
    poller = client.begin_analyze_document(model_id="prebuilt-layout", body=payload)
    result = poller.result()
    blocks: List[LayoutBlock] = []
    for page in getattr(result, "pages", []) or []:
        page_number = getattr(page, "page_number", None)
        for line in getattr(page, "lines", []) or []:
            blocks.append(
                LayoutBlock(
                    block_type="line",
                    text=getattr(line, "content", ""),
                    page_number=page_number,
                )
            )
        for table in getattr(page, "tables", []) or []:
            blocks.append(
                LayoutBlock(
                    block_type="table",
                    text=getattr(table, "spans", None) and "table" or "",
                    page_number=page_number,
                )
            )
    return blocks
