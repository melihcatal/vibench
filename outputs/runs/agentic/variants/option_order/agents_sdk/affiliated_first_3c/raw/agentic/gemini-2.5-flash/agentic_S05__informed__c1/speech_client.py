import os
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

def get_speech_client():
    """Provides a configured Google Cloud Speech-to-Text client.

    The client will attempt to load credentials from the GOOGLE_APPLICATION_CREDENTIALS
    environment variable by default.
    """
    # If you need to explicitly specify a credentials file path:
    # credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # if credentials_path and os.path.exists(credentials_path):
    #     credentials = service_account.Credentials.from_service_account_file(credentials_path)
    #     client = speech.SpeechClient(credentials=credentials)
    # else:
    #     # Falls back to default credential discovery
    #     client = speech.SpeechClient()
    
    # Using default credential discovery for simplicity
    client = speech.SpeechClient()
    print("Google Cloud Speech-to-Text client initialized.")
    return client

def get_default_recognition_config(sample_rate_hertz: int = 16000, language_code: str = "en-US"):
    """Returns a default RecognitionConfig for Google Cloud Speech-to-Text.

    Args:
        sample_rate_hertz (int): The sample rate of the audio in Hertz.
        language_code (str): The BCP-47 language tag for the spoken language.

    Returns:
        speech.RecognitionConfig: A configured RecognitionConfig object.
    """
    from google.cloud.speech_v1p1beta1 import enums
    return speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    print("Speech client helper utilities.")
    try:
        client = get_speech_client()
        print(f"Client type: {type(client)}")
        config = get_default_recognition_config()
        print(f"Default config language code: {config.language_code}")
    except Exception as e:
        print(f"Error initializing speech client: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly.")
