import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def transcribe_audio(audio_path):
    authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.getenv("IBM_STT_URL"))
    with open(audio_path, "rb") as audio_file:
        result = speech_to_text.recognize(
            audio=audio_file, content_type="audio/wav"
        ).get_result()
    return result["results"][0]["alternatives"][0]["transcript"]
