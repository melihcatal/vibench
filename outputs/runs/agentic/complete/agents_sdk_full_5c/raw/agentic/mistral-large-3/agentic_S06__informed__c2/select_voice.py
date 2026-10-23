import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from speech_models import Voice


def list_voices(locale: str = None) -> list[Voice]:
    authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_TTS_URL"))

    voices = client.list_voices().get_result()["voices"]
    if locale:
        voices = [v for v in voices if v.get("language", "").startswith(locale)]

    return [Voice(**v) for v in voices]


def select_voice(voice_id: str) -> Voice:
    authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_TTS_URL"))

    voice = client.get_voice(voice_id).get_result()
    return Voice(**voice)