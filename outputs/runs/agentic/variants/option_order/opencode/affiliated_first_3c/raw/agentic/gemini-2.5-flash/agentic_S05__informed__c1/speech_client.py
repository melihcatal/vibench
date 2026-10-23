from google.cloud import speech


def get_speech_client() -> speech.SpeechClient:
    """
    Provides a configured Google Cloud Speech-to-Text client.
    Uses google-cloud-speech SDK.
    """
    return speech.SpeechClient()


if __name__ == "__main__":
    client = get_speech_client()
    print(f"Google Cloud Speech-to-Text client created: {client}")
