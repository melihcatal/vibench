import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(os.getenv("IBM_STT_URL"))


def submit_transcription(audio_file):
    with open(audio_file, "rb") as audio:
        response = speech_to_text.create_job(
            audio,
            "audio/wav",
            {"word_alternatives_threshold": 0.9, "max_alternatives": 3},
        )
        return response.get_result()
