from speech_client import get_tts_client
from speech_models import (
    AudioOutputFormat,
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
)
from google.cloud import texttospeech


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Standard-A",
    audio_format: AudioOutputFormat = AudioOutputFormat.MP3,
) -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        language_code: The BCP-47 language code, e.g., "en-US".
        voice_name: The name of the voice to use, e.g., "en-US-Standard-A".
        audio_format: The desired audio output format.

    Returns:
        The audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_format.name)
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )

    return response.audio_content
