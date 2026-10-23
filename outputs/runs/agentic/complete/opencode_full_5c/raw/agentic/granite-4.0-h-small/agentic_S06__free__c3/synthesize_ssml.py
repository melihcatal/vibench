# same-scenario implementation - synthesize SSML to audio using Azure Cognitive Services

from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer
from speech_models import normalize_synth_response
from speech_client import get_azure_client

# Azure provider identification via SDK import (azure.cognitiveservices.speech)


async def synthesize_ssml(
    ssml: str, voice_name: str = None, locale: str = "en-US"
) -> bytes:
    """Synthesize SSML markup to a WAV byte stream using Azure TTS."""
    client = get_azure_client()
    speech_config = SpeechConfig(subscription=client.api_key, endpoint=client.endpoint)
    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name
    audio_config = AudioConfig(output_format=AudioConfig.OutputFormat.Wav)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = await synthesizer.speak_ssml_async(ssml)
    return normalize_synth_response(result)
