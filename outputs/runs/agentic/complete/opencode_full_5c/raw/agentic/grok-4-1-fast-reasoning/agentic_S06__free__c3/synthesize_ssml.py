from speech_client import get_tts_client
from speech_models import (
    create_ssml_input,
    create_voice_params,
    create_audio_config,
    SsmlVoiceGender,
)


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: str | None = None,
    ssml_gender: str | None = None,
    **audio_kwargs,
) -> bytes:
    client = get_tts_client()
    synthesis_input = create_ssml_input(ssml)
    gender_enum = SsmlVoiceGender[ssml_gender.upper()] if ssml_gender else None
    voice_params = create_voice_params(language_code, voice_name, gender_enum)
    audio_config = create_audio_config(**audio_kwargs)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content
