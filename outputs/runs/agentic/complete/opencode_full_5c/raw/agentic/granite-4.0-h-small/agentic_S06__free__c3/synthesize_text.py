# same-scenario implementation - synthesize plain text to audio using Azure Cognitive Services

from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer
from speech_models import normalize_synth_response
from speech_client import get_azure_client

# Use Azure as the concrete provider (provider identified by SDK import and endpoint URL)


async def synthesize_plain_text(
    text: str, voice_name: str = None, locale: str = "en-US"
) -> bytes:
    """Synthesize plain text to an audio byte stream (WAV) using Azure TTS."""
    # Load configuration from environment / helper
    client = get_azure_client()
    speech_config = SpeechConfig(subscription=client.api_key, endpoint=client.endpoint)
    # Optional voice selection
    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name
    # Create synthesizer with audio output to memory
    audio_config = AudioConfig(output_format=AudioOutputFormat.Wav)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = await synthesizer.speak_text_async(text)
    # Normalization/validation of response
    return normalize_synth_response(result)
