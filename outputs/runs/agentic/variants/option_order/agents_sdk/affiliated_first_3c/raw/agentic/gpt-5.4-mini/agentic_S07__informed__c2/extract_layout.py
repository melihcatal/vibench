from __future__ import annotations

from typing import List, Union

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_client
from document_models import DocumentInput, LayoutElement, LayoutExtractionResult

PROVIDER = "azure-document-intelligence"
MODEL_ID = "prebuilt-layout"


def extract_layout(document: Union[DocumentInput, str]) -> LayoutExtractionResult:
    client = get_client()
    source_url = document.source_url if isinstance(document, DocumentInput) else str(document)
    poller = client.begin_analyze_document(
        model_id=MODEL_ID,
        analyze_request=AnalyzeDocumentRequest(url_source=source_url),
    )
    result = poller.result()
    elements: List[LayoutElement] = []
    for paragraph in getattr(result, "paragraphs", []) or []:
        elements.append(
            LayoutElement(
                kind=getattr(paragraph, "role", "paragraph") or "paragraph",
                content=getattr(paragraph, "content", "") or "",
                page_number=getattr(paragraph, "page_number", None),
                bounding_regions=[br.as_dict() if hasattr(br, "as_dict") else getattr(br, "__dict__", {}) for br in getattr(paragraph, "bounding_regions", []) or []],
            )
        )
    for table in getattr(result, "tables", []) or []:
        elements.append(
            LayoutElement(
                kind="table",
                content="\n".join(cell.content for row in getattr(table, "cells", []) or [] for cell in [row]),
                page_number=getattr(table, "bounding_regions", [None])[0].page_number if getattr(table, "bounding_regions", None) else None,
                bounding_regions=[br.as_dict() if hasattr(br, "as_dict") else getattr(br, "__dict__", {}) for br in getattr(table, "bounding_regions", []) or []],
            )
        )
    return LayoutExtractionResult(elements=elements, provider=PROVIDER, model_id=MODEL_ID)
