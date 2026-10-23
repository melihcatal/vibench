import os
from google.cloud import texttospeech
from model_models import SpokenBriefRequest, SpokenBriefResponse


class GoogleCloudTextToSpeechClient:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def generate_spoken_brief(self, request: SpokenBriefRequest) -> SpokenBriefResponse:
        synthesis_input = texttospeech.SynthesisInput(text=request.text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=request.language_code,
            name=request.voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Default to neutral
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return SpokenBriefResponse(audio_content=response.audio_content)


def generate_spoken_brief_from_output(
    request: SpokenBriefRequest,
) -> SpokenBriefResponse:
    client = GoogleCloudTextToSpeechClient()
    return client.generate_spoken_brief(request)
