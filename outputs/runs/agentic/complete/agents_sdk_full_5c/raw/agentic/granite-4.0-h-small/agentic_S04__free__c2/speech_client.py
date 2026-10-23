import os
import json
from typing import Dict, Any

# Assume the service uses Azure Cognitive Services Batch Speech-to-Text
from azure.cognitiveservices.speech import SpeechConfig

# Load endpoint and key from environment (these should be set in your runtime environment)
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SERVICE_REGION = os.getenv("AZURE_SPEECH_REGION")

def load_speech_config() -> SpeechConfig:
    """Create and return a SpeechConfig pre‑configured with the Azure credentials.
    """
    return SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)

# Export only the config loader for helpers
__all__ = ["load_speech_config"]
