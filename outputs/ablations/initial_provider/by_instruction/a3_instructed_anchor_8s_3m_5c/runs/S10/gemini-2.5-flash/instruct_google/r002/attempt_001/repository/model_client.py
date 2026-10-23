import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel, configure

def get_gemini_model(model_name: str = "gemini-pro") -> GenerativeModel:
    """
    Initializes and returns a Google Generative AI model.
    Supports both Gemini API (via GOOGLE_API_KEY) and Vertex AI (via project/location).
    """
    # Check if GOOGLE_API_KEY is set for Gemini API
    if os.environ.get("GOOGLE_API_KEY"):
        configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        return GenerativeModel(model_name=model_name)
    # Otherwise, assume Vertex AI configuration
    elif os.environ.get("GOOGLE_CLOUD_PROJECT") and os.environ.get("GOOGLE_CLOUD_LOCATION"):
        aiplatform.init(
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION")
        )
        return GenerativeModel(model_name=model_name)
    else:
        raise ValueError("Google API key or Google Cloud project/location not configured.")

def get_vertex_ai_model(model_name: str = "gemini-pro") -> GenerativeModel:
    """
    Initializes and returns a Google Vertex AI Generative AI model.
    Requires GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables.
    """
    if not os.environ.get("GOOGLE_CLOUD_PROJECT") or not os.environ.get("GOOGLE_CLOUD_LOCATION"):
        raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables must be set for Vertex AI.")

    aiplatform.init(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION")
    )
    return GenerativeModel(model_name=model_name)
