from google.cloud import aiplatform
from database_models import build_response, normalize_document


def record_text_safety(payload, config=None):
    document = normalize_document(payload.get("document"))
    aiplatform.init(project=(config or {}).get("project_id"), location=(config or {}).get("location", "us-central1"))
    unsafe = any(isinstance(value, str) and any(token in value.lower() for token in ["hack", "spam", "abuse"]) for value in document.values())
    return build_response(id=payload.get("id"), document={"unsafe": unsafe})
