import os
import vertexai
from vertexai.generative_models import GenerativeModel

_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

_model = None


def get_model(model_name: str = "gemini-1.5-flash-001") -> GenerativeModel:
    global _model
    if not _model:
        vertexai.init(project=_PROJECT_ID, location=_LOCATION)
        _model = GenerativeModel(model_name)
    return _model
