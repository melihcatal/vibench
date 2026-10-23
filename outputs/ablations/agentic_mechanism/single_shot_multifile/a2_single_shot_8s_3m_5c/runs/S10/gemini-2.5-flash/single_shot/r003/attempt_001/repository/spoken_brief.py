from model_client import LLMClientFactory
from model_models import SpokenBriefRequest, SpokenBriefResponse
from google.cloud import texttospeech
import os

def generate_spoken_brief(request: SpokenBriefRequest) -> SpokenBriefResponse:
    client = LLMClientFactory.get_google_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config
    )

    return SpokenBriefResponse(
        audio_content=response.audio_content,
        audio_format="LINEAR16"
    )