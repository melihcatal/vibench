import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig

def get_speech_config(api_key: str = None, region: str = None) -> SpeechConfig:
    api_key = api_key or os.environ.get("AZURE_SPEECH_KEY")
    region = region or os.environ.get("AZURE_SPEECH_REGION")

    if not api_key or not region:
        raise ValueError("Azure Speech API key and region must be provided or set as environment variables AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.")

    return speechsdk.SpeechConfig(subscription=api_key, region=region)
