import re

from database_models import DocumentResponse, normalize_document


_unsafe = re.compile(r"(?:\b(?:hate|violence|weapon|explosive)\b|<script[^>]*>)", re.I)


def check_text_safety(record):
    doc = normalize_document(record) or {}
    text = " ".join(str(doc.get(k, "")) for k in ("title", "text", "description"))
    unsafe = bool(_unsafe.search(text))
    return DocumentResponse(
        ok=not unsafe, data={"unsafe": unsafe, "document_id": doc.get("document_id")}
    ).__dict__


def handler(event, context=None):
    return check_text_safety(event.get("record", event))
