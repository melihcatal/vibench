import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    azure_speech_key: str
    azure_speech_region: str
    openai_api_key: str
    openai_model: str


def load_config() -> SpeechConfig:
    return SpeechConfig(
        azure_speech_key=os.environ.get("AZURE_SPEECH_KEY", ""),
        azure_speech_region=os.environ.get("AZURE_SPEECH_REGION", "eastus"),
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        openai_model=os.environ.get("OPENAI_MODEL", "gpt-5.4-mini"),
    )


def azure_tts_endpoint(region: str) -> str:
    return f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"


def openai_base_url() -> str:
    return "https://api.openai.com/v1"
