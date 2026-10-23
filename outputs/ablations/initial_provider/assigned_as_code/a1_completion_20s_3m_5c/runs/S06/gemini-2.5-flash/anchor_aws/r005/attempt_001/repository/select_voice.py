from speech_client import get_text_to_speech_client
from speech_models import Voice, ListVoicesResponse
from google.cloud import texttospeech

def list_voices(language_code: str = None) -> ListVoicesResponse:
    client = get_text_to_speech_client()
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append(Voice(
            name=voice.name,
            language_codes=list(voice.language_codes),
            ssml_gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            natural_voice_profile=voice.natural_voice_profile
        ))
    return ListVoicesResponse(voices=voice_list)

def select_voice_by_name(voice_name: str, language_code: str = None) -> Voice:
    all_voices = list_voices(language_code=language_code).voices
    for voice in all_voices:
        if voice.name == voice_name:
            return voice
    return None

def select_voice_by_gender(language_code: str, ssml_gender: str) -> Voice:
    all_voices = list_voices(language_code=language_code).voices
    for voice in all_voices:
        if voice.ssml_gender == ssml_gender.upper():
            return voice
    return None
