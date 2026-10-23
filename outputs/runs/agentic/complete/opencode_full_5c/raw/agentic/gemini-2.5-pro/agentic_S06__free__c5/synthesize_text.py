from google.cloud import texttospeech
from speech_client import get_speech_client
from speech_models import SynthesisRequest, SpeechRequest, VoiceSelection, AudioConfig


def synthesize_text(text: str, voice_name: str = "en-US-Studio-M"):
    """
    Synthesizes speech from the input string of text.

    Args:
        text (str): The text to synthesize.
        voice_name (str): The name of the voice to use.

    Returns:
        bytes: The audio content of the synthesized speech.
    """
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
