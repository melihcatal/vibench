import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Expect environment variables IBM_TTS_APIKEY and IBM_TTS_URL


class ReviewerBriefAudio:
    def __init__(self):
        authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
        self.tts = TextToSpeechV1(authenticator=authenticator)
        self.tts.set_service_url(os.getenv("IBM_TTS_URL"))

    def generate_spoken_brief(self, brief_text: str, output_path: str) -> None:
        accept = "audio/wav"
        with open(output_path, "wb") as audio_file:
            response = self.tts.synthesize(
                brief_text, accept=accept, voice="en-US_MichaelV3Voice"
            )
            audio_file.write(response.get_result().content)
