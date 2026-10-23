import os
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech

# -------------------
# Client configuration
# -------------------
# Load credentials from environment
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS to path of JSON key file")


# Helper to create a speech client
def get_google_client() -> speech.SpeechClient:
    """Create and return a configured Speech-to-Text client."""
    client = speech.SpeechClient()
    return client


# Optional: custom timeout configuration (seconds)
DEFAULT_TIMEOUT = 60  # adjust as needed


def create_stt_client(timeout: Optional[int] = DEFAULT_TIMEOUT) -> speech.SpeechClient:
    # The default client already respects GOOGLE_APPLICATION_CREDENTIALS; timeout can be used
    # when calling individual methods if the client library supports it.
    return speech.SpeechClient()


# Example usage (kept for reference)
if __name__ == "__main__":
    client = get_google_client()
    print("Google Speech client ready")
