import os
from google.cloud import texttospeech
from model_models import AudioBriefingRequest, AudioBriefingResponse


def generate_google_cloud_audio_briefing(
    request: AudioBriefingRequest,
) -> AudioBriefingResponse:
    # Provider-identifying signal: google-cloud-texttospeech SDK
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,  # e.g., "en-US-Wavenet-D"
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioBriefingResponse(audio_content=response.audio_content)
