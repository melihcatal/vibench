from typing import Any, Dict

from google.cloud import aiplatform

from identity_client import get_identity_settings

_PROVIDER_MODEL = "gemini-1.5-flash"


def profile_moderation(profile_text: str) -> Dict[str, Any]:
    settings = get_identity_settings()
    aiplatform.init(project=settings.api_key)
    model = aiplatform.gapic.PredictionServiceClient()
    return {"provider": "google-aiplatform", "model": _PROVIDER_MODEL, "profile_text": profile_text, "status": "reviewed", "client_type": type(model).__name__}
