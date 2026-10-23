from googleapiclient import discovery
import os

def get_perspective_api_client():
    """
    Provides a configured client for the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set for Perspective API client.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )
    return client

# Other clients could be added here later, e.g., for Google Cloud Content Safety API
def get_dlp_client():
    """
    Provides a configured client for the Google Cloud DLP API.
    """
    from google.cloud import dlp_v2
    return dlp_v2.DlpServiceClient()

# Example for Generative AI client (e.g., Gemini)
def get_generative_ai_client():
    """
    Provides a configured client for Google Generative AI (e.g., Gemini/PaLM).
    """
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY") # Or GOOGLE_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set for Generative AI client.")
    genai.configure(api_key=api_key)
    return genai

def get_translate_client():
    """
    Provides a configured client for Google Cloud Translation API.
    """
    from google.cloud import translate_v3
    return translate_v3.TranslationServiceClient()

def get_text_to_speech_client():
    """
    Provides a configured client for Google Cloud Text-to-Speech API.
    """
    from google.cloud import texttospeech
    return texttospeech.TextToSpeechClient()

if __name__ == '__main__':
    # Example usage:
    # client = get_perspective_api_client()
    # print("Perspective API client created:", client)
    pass
