from document_client import get_client, open_document
from document_models import LayoutElement, normalize_text


def extract_layout(source: str):
    client = get_client()
    doc = open_document(source)
    if hasattr(doc, "read"):
        poller = client.begin_analyze_document("prebuilt-layout", doc)
    else:
        poller = client.begin_analyze_document_from_url("prebuilt-layout", doc)
    result = poller.result()
    elements = []
    for block in getattr(result, "paragraphs", []) or []:
        elements.append(
            LayoutElement(
                kind="paragraph",
                text=normalize_text(getattr(block, "content", "")),
                polygon=getattr(block, "polygon", None),
                raw=block,
            )
        )
    for table in getattr(result, "tables", []) or []:
        elements.append(
            LayoutElement(
                kind="table",
                text=normalize_text(getattr(table, "caption", "")),
                polygon=getattr(table, "bounding_regions", None),
                raw=table,
            )
        )
    return elements
