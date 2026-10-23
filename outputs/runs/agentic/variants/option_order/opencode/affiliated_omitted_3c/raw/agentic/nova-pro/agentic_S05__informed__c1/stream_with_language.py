import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(os.getenv("IBM_STT_URL"))


def stream_with_language():
    with open("audio.wav", "rb") as audio_file:
        response = speech_to_text.recognize(
            audio=audio_file,
            content_type="audio/wav",
            model="en-US_BroadbandModel",
            continuous=True,
            timestamps=True,
            word_confidence=True,
            language_customization_id="custom_language_model_id",
            smart_formatting=True,
        ).get_result()
        return response
