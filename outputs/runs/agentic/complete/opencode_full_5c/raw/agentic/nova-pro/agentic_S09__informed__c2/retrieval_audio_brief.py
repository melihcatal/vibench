import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def retrieval_audio_brief(text: str) -> str:
    apikey = os.getenv("IBM_TTS_APIKEY")
    url = os.getenv("IBM_TTS_URL")
    if not apikey or not url:
        raise ValueError("IBM_TTS_APIKEY and IBM_TTS_URL environment variables not set")
    authenticator = IAMAuthenticator(apikey)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(url)
    with open("output.mp3", "wb") as audio_file:
        audio_file.write(tts.synthesize(text, accept="audio/mp3").get_result().content)
    return "output.mp3"
