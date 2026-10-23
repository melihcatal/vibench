import os
from google.cloud import texttospeech

def get_text_to_speech_client():
    """Provides a configured Google Cloud Text-to-Speech client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    # Google Cloud Text-to-Speech client setup
    # The client will automatically use credentials from GOOGLE_APPLICATION_CREDENTIALS
    # or other standard Google Cloud authentication methods.
    client = texttospeech.TextToSpeechClient()
    return client

def get_default_voice_params(language_code: str = "en-US", name: str = "en-US-Standard-C"):
    """Returns default voice selection parameters."""
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=name
    )

def get_default_audio_config(audio_encoding=texttospeech.AudioEncoding.MP3):
    """Returns default audio configuration."""
    return texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

if __name__ == "__main__":
    # Example usage
    try:
        client = get_text_to_speech_client()
        print("Google Cloud Text-to-Speech client initialized successfully.")
        # You can test a simple operation if credentials are set up
        # For example, listing voices:
        # voices = client.list_voices().voices
        # print(f"Found {len(voices)} voices.")
    except Exception as e:
        print(f"Error initializing client: {e}")
