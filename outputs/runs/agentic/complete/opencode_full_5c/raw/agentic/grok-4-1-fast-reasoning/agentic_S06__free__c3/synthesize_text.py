from speech_client import get_tts_client
from speech_models import create_text_input, create_voice_params, create_audio_config


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: str | None = None,
    **audio_kwargs,
) -> bytes:
    client = get_tts_client()
    synthesis_input = create_text_input(text)
    voice_params = create_voice_params(language_code, voice_name)
    audio_config = create_audio_config(**audio_kwargs)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content
