import os
from typing import Dict

# Azure Speech credentials (replace with your own)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def get_speech_config() -> Dict[str, str]:
    """Returns a dict with Azure TTS credentials suitable for SDK configuration.

    Returns:
        dict: Keys `subscription` and `region` to initialize `SpeechConfig`.
    """
    return {
        "subscription": AZURE_SPEECH_KEY,
        "region": AZURE_SPEECH_REGION,
    }


def init_speech_synthesizer() -> "SpeechSynthesizer":  # type: ignore
    """Initialize an Azure TTS Speech Synthesizer from environment variables.

    Returns:
        SpeechSynthesizer: Ready-to-use TTS client instance.
    """
    from azure.cognitiveservices.speech import (
        SpeechConfig,
        AudioConfig,
        SpeechSynthesizer,
    )

    cfg = get_speech_config()
    speech_config = SpeechConfig(subscription=cfg["subscription"], region=cfg["region"])
    audio_config = AudioConfig(output_format="Riff24Khz16BitMonoPcm")
    return SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


# Example (commented out) usage
# client = init_speech_synthesizer()
