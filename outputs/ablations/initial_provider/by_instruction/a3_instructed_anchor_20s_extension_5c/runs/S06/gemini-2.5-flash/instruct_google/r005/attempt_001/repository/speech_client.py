from google.cloud import texttospeech

def get_text_to_speech_client():
    """Provides a Google Cloud Text-to-Speech client instance."""
    return texttospeech.TextToSpeechClient()

# Example of potential centralized configuration (if needed)
def get_default_voice_params():
    return texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

def get_default_audio_config():
    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
