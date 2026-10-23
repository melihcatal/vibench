import os
from google.cloud import texttospeech
from model_models import SpokenBriefRequest

# Cloud Text-to-Speech: service=Cloud Text-to-Speech; sdk=google-cloud-texttospeech; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS


def generate_spoken_brief(request: SpokenBriefRequest) -> bytes:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    # For local testing, ensure your gcloud is authenticated or GOOGLE_APPLICATION_CREDENTIALS points to a service account key file.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Or other genders as needed
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # Or other formats like LINEAR16, OGG_OPUS
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The audio content is a binary stream
    return response.audio_content
