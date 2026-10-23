import os
from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from speech_models import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
)


def synthesize_ssml(
    ssml: str, voice_params: VoiceSelectionParams, audio_config: AudioConfig
) -> bytes:
    client = get_text_to_speech_client()
    synthesis_input = SynthesisInput(ssml=ssml)

    response = client.synthesize_speech(
        input=synthesis_input.to_google_cloud(),
        voice=voice_params.to_google_cloud(),
        audio_config=audio_config.to_google_cloud(),
    )
    return response.audio_content
