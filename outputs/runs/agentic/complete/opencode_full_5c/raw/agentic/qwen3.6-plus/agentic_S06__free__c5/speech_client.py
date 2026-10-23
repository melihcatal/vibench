import os
from google.cloud import texttospeech


def get_tts_client(credentials_path=None):
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return texttospeech.TextToSpeechClient()


def get_synthesis_input(text=None, ssml=None):
    if ssml is not None:
        return texttospeech.SynthesisInput(ssml=ssml)
    return texttospeech.SynthesisInput(text=text or "")


def get_voice_selection(language_code=None, name=None, ssml_gender=None):
    selection = texttospeech.VoiceSelectionParams()
    if language_code:
        selection.language_code = language_code
    if name:
        selection.name = name
    if ssml_gender:
        selection.ssml_gender = texttospeech.SsmlVoiceGender[ssml_gender.upper()]
    return selection


def get_audio_config(
    audio_encoding="MP3", speaking_rate=1.0, pitch=0.0, volume_gain_db=0.0
):
    encoding_map = {
        "MP3": texttospeech.AudioEncoding.MP3,
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        "MULAW": texttospeech.AudioEncoding.MULAW,
        "ALAW": texttospeech.AudioEncoding.ALAW,
    }
    config = texttospeech.AudioConfig(
        audio_encoding=encoding_map.get(audio_encoding, texttospeech.AudioEncoding.MP3),
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )
    return config


def build_synthesis_request(
    text=None,
    ssml=None,
    language_code=None,
    voice_name=None,
    ssml_gender=None,
    audio_encoding="MP3",
    speaking_rate=1.0,
    pitch=0.0,
    volume_gain_db=0.0,
    effects_profile_id=None,
):
    input_data = get_synthesis_input(text=text, ssml=ssml)
    voice = get_voice_selection(
        language_code=language_code, name=voice_name, ssml_gender=ssml_gender
    )
    audio = get_audio_config(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )
    request = texttospeech.SynthesizeSpeechRequest(
        input=input_data,
        voice=voice,
        audio_config=audio,
    )
    if effects_profile_id:
        request.audio_config.effects_profile_id = (
            [effects_profile_id]
            if isinstance(effects_profile_id, str)
            else effects_profile_id
        )
    return request


def synthesize_audio(client, request):
    response = client.synthesize_speech(request=request)
    return response.audio_content


def list_voices(client, language_code=None):
    request = texttospeech.ListVoicesRequest(language_code=language_code)
    response = client.list_voices(request=request)
    return response.voices


def get_default_voice_for_locale(locale="en-US"):
    voice_map = {
        "en-US": "en-US-Neural2-F",
        "en-GB": "en-GB-Neural2-A",
        "es-ES": "es-ES-Neural2-A",
        "fr-FR": "fr-FR-Neural2-A",
        "de-DE": "de-DE-Neural2-A",
        "ja-JP": "ja-JP-Neural2-B",
        "zh-CN": "zh-CN-Neural2-A",
        "ko-KR": "ko-KR-Neural2-A",
        "pt-BR": "pt-BR-Neural2-A",
        "it-IT": "it-IT-Neural2-A",
    }
    return voice_map.get(locale, "en-US-Neural2-F")
