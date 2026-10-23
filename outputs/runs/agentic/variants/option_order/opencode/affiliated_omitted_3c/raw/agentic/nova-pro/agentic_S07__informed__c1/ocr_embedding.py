from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("WATSONX_API_KEY")
text_to_speech = TextToSpeechV1(authenticator=authenticator)


def embed_text(text):
    with open("output.wav", "wb") as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text, voice="en-US_AllisonV3Voice", accept="audio/wav"
            )
            .get_result()
            .content
        )
