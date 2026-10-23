from database_models import build_response


def record_summary(payload, config=None):
    document = payload.get("document") or {}
    summary = {
        "id": document.get("id") or payload.get("id"),
        "title": document.get("title") or document.get("name") or "",
        "summary": document.get("summary") or document.get("description") or "",
    }
    return build_response(summary)
