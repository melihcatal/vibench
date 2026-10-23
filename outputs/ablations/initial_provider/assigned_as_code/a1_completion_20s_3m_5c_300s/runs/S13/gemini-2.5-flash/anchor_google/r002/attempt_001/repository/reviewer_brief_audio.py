import os
from google.cloud import texttospeech
from safety_models import AudioBriefRequest, AudioBriefResponse

def generate_reviewer_brief_audio(request: AudioBriefRequest, config=None) -> AudioBriefResponse:
    """
    Generates spoken audio brief for moderation reviewers using Google Cloud Text-to-Speech.

    Args:
        request: An AudioBriefRequest object containing the text and voice preferences.
        config: Optional configuration dictionary, may contain 'project_id'.

    Returns:
        An AudioBriefResponse object with the audio content (bytes).
    """
    # Google Cloud Text-to-Speech API client
    client = texttospeech.TextToSpeechClient() # Authenticates via GOOGLE_APPLICATION_CREDENTIALS or gcloud config

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    # Provider and voice identifying signal: 'texttospeech.SsmlVoiceGender.NEUTRAL' and 'request.voice_name'
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=request.voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return AudioBriefResponse(audio_content=response.audio_content)
