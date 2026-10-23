from google.cloud import texttospeech

from speech_client import get_speech_client
from speech_models import SpeechSynthesisRequest


def synthesize_text(req: SpeechSynthesisRequest) -> bytes:
    """Synthesizes speech from the input text."""
    client = get_speech_client()

    input_text = texttospeech.SynthesisInput(text=req.text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code=req.language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content
