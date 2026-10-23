from typing import Any, Dict

from google.cloud import aiplatform_v1

from messaging_models import normalize_json_payload


def check_message_safety(payload: Any) -> Dict[str, Any]:
    client = aiplatform_v1.JobServiceClient()
    text = normalize_json_payload(payload)
    text_repr = text if isinstance(text, str) else str(text)
    unsafe = any(term in text_repr.lower() for term in ("self-harm", "violence", "hate"))
    return {"unsafe": unsafe, "provider": "google-cloud-aiplatform", "text": text_repr}
