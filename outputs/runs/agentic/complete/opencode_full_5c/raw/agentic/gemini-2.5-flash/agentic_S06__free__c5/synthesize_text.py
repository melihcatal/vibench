from google.cloud import texttospeech
from speech_client import get_tts_client, get_default_audio_config


def synthesize_text(
    text: str, language_code: str = "en-US", name: str = "en-US-Standard-A"
) -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        language_code: The language code for the voice (e.g., "en-US").
        name: The name of the voice to use (e.g., "en-US-Standard-A").

    Returns:
        The audio content as a byte string.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=name,
    )

    audio_config = get_default_audio_config()

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
