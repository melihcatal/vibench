from google.cloud import texttospeech
import os

def get_tts_client():
    """Returns an initialized Google Cloud Text-to-Speech client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return texttospeech.TextToSpeechClient()


# You could also define configuration here, e.g., default voice settings
def get_default_voice_params():
    """Returns default voice selection parameters.
    """
    return texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

def get_default_audio_config():
    """Returns default audio configuration parameters.
    """
    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )


if __name__ == '__main__':
    client = get_tts_client()
    print(f"Successfully initialized TextToSpeechClient: {client}")
    voice_params = get_default_voice_params()
    print(f"Default voice name: {voice_params.name}")
