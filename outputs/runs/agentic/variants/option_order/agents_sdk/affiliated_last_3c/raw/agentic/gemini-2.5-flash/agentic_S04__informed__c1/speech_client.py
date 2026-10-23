import os
from dataclasses import dataclass

@dataclass
class SpeechConfig:
    speech_key: str
    speech_region: str

def get_speech_config() -> SpeechConfig:
    # Azure AI Speech credentials
    # Set these environment variables: AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    
    return SpeechConfig(speech_key=speech_key, speech_region=speech_region)
