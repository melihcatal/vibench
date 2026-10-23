from speech_client import get_tts_client
from speech_models import create_synthesis_input, create_voice_selection_params, create_audio_config
from typing import Optional

def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: Optional[str] = None,
    ssml_gender_str: Optional[str] = None,
    **audio_config_kwargs
) -> bytes:
    client = get_tts_client()
    synthesis_input = create_synthesis_input(text=text)
    voice_params = create_voice_selection_params(
        language_code=language_code,
        name=voice_name,
        ssml_gender_str=ssml_gender_str
    )
    audio_config = create_audio_config(**audio_config_kwargs)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )
    return response.audio_content
