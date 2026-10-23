import os
from speech_client import get_tts_client
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_text(
    text: str, voice_id: str = None, language_code: str = "en-US"
) -> bytes:
    """
    Synthesize plain text to audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()

    if voice_id is None:
        voice_id = "en-US-Neural2-J"

    synthesis_input = {"text": text}

    voice_config = {
        "language_code": language_code,
        "name": voice_id,
        "ssml_gender": "FEMALE",
    }

    audio_config = {"audio_encoding": "MP3"}

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice_config, audio_config=audio_config
        )

        audio_content = response.audio_content
        return audio_content

    except Exception as e:
        raise Exception(f"Text synthesis failed: {str(e)}")
