from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import SynthesisResponse


def synthesize_ssml(ssml_text: str) -> bytes:
    """Synthesizes speech from the input string of SSML."""
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Note: Voice and prosody are controlled within the SSML itself.
    # Example SSML:
    # <speak>
    #   <voice name="en-US-Wavenet-D">
    #     <prosody rate="slow">Hello, world!</prosody>
    #   </voice>
    # </speak>
    voice = texttospeech.VoiceSelectionParams(language_code="en-US")

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
