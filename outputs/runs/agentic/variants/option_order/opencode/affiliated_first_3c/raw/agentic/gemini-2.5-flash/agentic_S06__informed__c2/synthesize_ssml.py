from speech_client import get_tts_client
from speech_models import (
    AudioOutputFormat,
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
)
from google.cloud import texttospeech


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Standard-A",
    audio_format: AudioOutputFormat = AudioOutputFormat.MP3,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> bytes:
    """Synthesizes SSML to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        ssml: The SSML text to synthesize.
        language_code: The BCP-47 language code, e.g., "en-US".
        voice_name: The name of the voice to use, e.g., "en-US-Standard-A".
        audio_format: The desired audio output format.
        speaking_rate: The speaking rate, 0.25 to 4.0. 1.0 is normal.
        pitch: The pitch, -20.0 to 20.0. 0.0 is normal.

    Returns:
        The audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_format.name),
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )

    return response.audio_content
