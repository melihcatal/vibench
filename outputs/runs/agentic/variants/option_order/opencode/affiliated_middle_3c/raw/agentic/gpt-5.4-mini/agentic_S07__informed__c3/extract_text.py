from document_client import get_client, open_document
from document_models import OCRResult, normalize_text, page_dict


def extract_text(source: str) -> OCRResult:
    client = get_client()
    doc = open_document(source)
    with doc if hasattr(doc, "read") else None:
        if hasattr(doc, "read"):
            poller = client.begin_analyze_document("prebuilt-read", doc)
        else:
            poller = client.begin_analyze_document_from_url("prebuilt-read", doc)
    result = poller.result()
    text = normalize_text(getattr(result, "content", ""))
    pages = [page_dict(p) for p in getattr(result, "pages", [])]
    return OCRResult(text=text, pages=pages, raw=result)
