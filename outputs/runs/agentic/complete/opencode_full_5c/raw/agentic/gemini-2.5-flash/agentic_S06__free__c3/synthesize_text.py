from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import SynthesisInput, VoiceConfig, AudioConfig


def synthesize_text(
    text: str, voice_config: VoiceConfig, audio_config: AudioConfig
) -> bytes:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=voice_config.language_code,
        name=voice_config.name,
        ssml_gender=texttospeech.SsmlVoiceGender[voice_config.ssml_gender]
        if voice_config.ssml_gender
        else None,
    )

    audio_config_params = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[audio_config.audio_encoding],
        speaking_rate=audio_config.speaking_rate,
        pitch=audio_config.pitch,
        volume_gain_db=audio_config.volume_gain_db,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config_params,
    )

    return response.audio_content
