from google.cloud import texttospeech

def get_text_to_speech_client():
    """
    Provides a Google Cloud Text-to-Speech client instance.
    The client will automatically pick up credentials from the environment
    (e.g., GOOGLE_APPLICATION_CREDENTIALS).
    """
    return texttospeech.TextToSpeechClient()

if __name__ == "__main__":
    # Example usage
    client = get_text_to_speech_client()
    print("Google Cloud Text-to-Speech client initialized:", client)
