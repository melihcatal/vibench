from typing import Dict, Any
from model_models import ChatResponse
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
import os


def generate_platform_brief_audio(
    response: ChatResponse,
    output_file: str = "brief_audio.wav",
) -> Dict[str, Any]:
    """
    Generates spoken briefings from Azure AI Inference model outputs using Azure Speech Services.
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    if not all([speech_key, service_region]):
        raise ValueError("Missing required Azure Speech Services configuration.")

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = AudioConfig(filename=output_file)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = synthesizer.speak_text_async(response.content).get()

    return {
        "output_file": output_file,
        "result_reason": result.reason.name,
        "audio_duration": result.audio_duration,
        "raw_result": result,
    }
