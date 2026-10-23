from google.cloud import speech_v1 as speech
import os


class TTSQATranscriber:
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe_audio(self, audio_content: bytes) -> str:
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=24000,
            language_code="en-US",
            model="latest_long",
        )
        response = self.client.recognize(config=config, audio=audio)

        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        return transcript
