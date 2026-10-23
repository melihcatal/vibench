import os
from google.genai import ServiceOptions


def get_model_client(model_name: str) -> object:
    """Returns a configured Google Gemini client based on environment variables.

    Args:
        model_name (str): Identifier for the client (e.g., 'gemini').

    Returns:
        google.genai.Services object configured for the provider.
    """
    # Gemini API key is set via GOOGLE_API_KEY env var
    service_options = ServiceOptions()
    service_options.api_key = os.getenv("GOOGLE_API_KEY")
    return service_options.get_gemini_client(model_name)
