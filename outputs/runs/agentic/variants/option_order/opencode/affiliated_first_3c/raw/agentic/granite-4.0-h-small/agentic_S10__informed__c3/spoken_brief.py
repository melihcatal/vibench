import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class SpokenBrief:
    def __init__(self):
        api_key = os.getenv("IBM_TTS_APIKEY")
        service_url = os.getenv("IBM_TTS_URL")
        self.authenticator = IAMAuthenticator(api_key)
        self.tts = TextToSpeechV1(authenticator=self.authenticator)
        self.tts.set_service_url(service_url)

    def generate_spoken(self, text):
        audio = self.tts.synthesize(text=text, accept="audio/wav")
        # Save to temporary file for playback (not required by task)
        with open("brief.wav", "wb") as audio_file:
            audio_file.write(audio.get_result().content)
        return "brief.wav"


if __name__ == "__main__":
    speaker = SpokenBrief()
    brief_text = "You have two unread messages. The first says Hello World."
    filename = speaker.generate_spoken(brief_text)
    print("Spoken audio saved as", filename)
