import os
from google.cloud import texttospeech
from embeddings_models import AudioBriefRequest, AudioBriefResponse


def generate_audio_brief(request: AudioBriefRequest) -> AudioBriefResponse:
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioBriefResponse(audio_content=response.audio_content)
