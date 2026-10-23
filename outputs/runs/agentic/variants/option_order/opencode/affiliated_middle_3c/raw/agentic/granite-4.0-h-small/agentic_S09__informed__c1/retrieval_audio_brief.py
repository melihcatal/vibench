import os
from google.cloud import texttospeech as tts  # example provider; replace as needed

def generate_spoken_brief(text: str) -> bytes:
    """
    Convert retrieved search result text into a spoken audio brief.

    Args:
        text (str): Text to synthesize.

    Returns:
        bytes: Audio data in the default WAV format.
    """
    api_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # path to service account JSON
    client = tts.TextToSpeechClient.from_service_account_json(api_key)
    input_ssml = tts.SynthesisInput(ssml=f\"<speak>{text}</speak>\")
    voice = tts.VoiceSelectionParams(language_code='en-US', name='en-US-Wavenet-D')
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    return response.audio_content
