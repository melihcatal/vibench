from __future__ import annotations

from typing import List, Optional

from document_client import DocumentServiceClient
from document_models import DocumentRequest, LayoutElement, LayoutResponse


def extract_layout(document_path: Optional[str] = None, document_bytes: Optional[bytes] = None) -> LayoutResponse:
    request = DocumentRequest(document_path=document_path, document_bytes=document_bytes)
    client = DocumentServiceClient()
    result = client.analyze(request, model_id="prebuilt-layout")
    elements: List[LayoutElement] = []
    for page_index, page in enumerate(getattr(result, "pages", []) or [], start=1):
        for line in getattr(page, "lines", []) or []:
            elements.append(LayoutElement(kind="line", text=getattr(line, "content", ""), page=page_index, metadata={"provider": "azure-document-intelligence"}))
    for table in getattr(result, "tables", []) or []:
        elements.append(LayoutElement(kind="table", text="table", page=None, metadata={"row_count": len(getattr(table, 'cells', []) or [])}))
    return LayoutResponse(elements=elements, provider="azure-document-intelligence", metadata={"model_id": "prebuilt-layout"})
