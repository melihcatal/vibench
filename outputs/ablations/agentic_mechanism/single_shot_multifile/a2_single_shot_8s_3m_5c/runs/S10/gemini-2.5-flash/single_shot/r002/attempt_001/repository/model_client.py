import os
import vertexai
import openai
from vertexai.generative_models import GenerativeModel

_gemini_models = {}
_openai_client = None

def get_gemini_model(project_id: str, location: str, model_name: str = "gemini-pro") -> GenerativeModel:
    key = f"{project_id}-{location}-{model_name}"
    if key not in _gemini_models:
        vertexai.init(project=project_id, location=location)
        _gemini_models[key] = GenerativeModel(model_name)
    return _gemini_models[key]

def get_openai_client() -> openai.OpenAI:
    global _openai_client
    if _openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        _openai_client = openai.OpenAI(api_key=api_key)
    return _openai_client
