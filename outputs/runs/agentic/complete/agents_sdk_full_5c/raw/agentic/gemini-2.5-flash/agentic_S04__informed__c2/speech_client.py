import os

def get_assemblyai_api_key() -> str:
    """Retrieves the AssemblyAI API key from environment variables."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return api_key

def get_google_translation_credentials():
    """Placeholder for Google Cloud Translation credentials setup."
    # Google Cloud client libraries automatically use GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if set. No explicit code needed here.
    pass

def get_azure_content_safety_config() -> dict:
    """Retrieves Azure AI Content Safety configuration from environment variables."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY not set.")
    return {"endpoint": endpoint, "key": key}

def get_google_gemini_api_key() -> str:
    """Retrieves the Google Gemini API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    return api_key
