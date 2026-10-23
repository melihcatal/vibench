import os
import google.cloud.texttospeech as tts

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service_key.json")

def get_texttospeech_client() -> tts.TextToSpeechClient:
    """Create and return a reusable Google Cloud Text‑to‑Speech client.

    Uses the environment variable GOOGLE_APPLICATION_CREDENTIALS for authentication.
    """
    return tts.TextToSpeechClient.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)

def get_texttospeech_client_default() -> tts.TextToSpeechClient:
    """Create client relying on Application Default Credentials (ADC).
    """
    return tts.TextToSpeechClient()

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     client = get_texttospeech_client()
#     print("Client created with credentials from", GOOGLE_APPLICATION_CREDENTIALS)
