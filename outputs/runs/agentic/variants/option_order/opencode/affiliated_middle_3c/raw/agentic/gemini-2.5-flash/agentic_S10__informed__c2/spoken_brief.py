import os
from google.cloud import texttospeech
from model_models import SpokenBriefRequest, SpokenBriefResponse


def generate_spoken_brief(request: SpokenBriefRequest) -> SpokenBriefResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text_content)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Only send the bytes.
    return SpokenBriefResponse(audio_content=response.audio_content)
