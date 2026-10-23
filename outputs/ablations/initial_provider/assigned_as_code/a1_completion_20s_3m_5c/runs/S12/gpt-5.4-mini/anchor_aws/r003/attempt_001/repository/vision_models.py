def normalize_label_response(response):
    return {"labels": [{"name": item["name"], "confidence": float(item["confidence"])} for item in response.get("labels", [])]}


def normalize_description_response(response):
    return {"description": str(response.get("description", ""))}


def normalize_text_response(response):
    return {"text": response.get("text", ""), "lines": response.get("lines", [])}


def normalize_safety_response(response):
    return {"unsafe": bool(response.get("unsafe", False)), "categories": response.get("categories", []), "summary": response.get("summary", "")}


def normalize_translation_response(response):
    return {"translation": str(response.get("translation", "")), "language": response.get("language", "")}


def normalize_archive_response(response):
    return {"uri": response.get("uri", ""), "etag": response.get("etag", ""), "content_type": response.get("content_type", "")}
