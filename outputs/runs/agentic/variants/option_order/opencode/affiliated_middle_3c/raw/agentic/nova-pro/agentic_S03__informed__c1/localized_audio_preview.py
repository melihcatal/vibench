import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def localized_audio_preview(text):
    api_key = os.getenv("WATSONX_API_KEY")
    url = os.getenv("WATSONX_URL")
    authenticator = IAMAuthenticator(api_key)
    text_to_speech = TextToSpeechV1(authenticator=authenticator)
    text_to_speech.set_service_url(url)
    with open("output.wav", "wb") as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text, accept="audio/wav", voice="en-US_AllisonV3Voice"
            )
            .get_result()
            .content
        )
