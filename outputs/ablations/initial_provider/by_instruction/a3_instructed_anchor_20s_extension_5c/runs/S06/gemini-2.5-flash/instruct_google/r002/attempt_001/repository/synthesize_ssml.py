from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import get_default_voice_params, get_default_audio_config

def synthesize_ssml(ssml_text: str, voice_name: str = "en-US-Standard-C", language_code: str = "en-US", ssml_gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.FEMALE) -> bytes:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = get_default_voice_params(language_code=language_code, name=voice_name, ssml_gender=ssml_gender)
    audio_config = get_default_audio_config()

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content
