import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config() -> speechsdk.SpeechConfig:
    """
    Provides the Azure AI Speech configuration.
    Reads AZURE_SPEECH_KEY and AZURE_SPEECH_REGION from environment variables.

    Returns:
        An initialized SpeechConfig object.
    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    return speech_config
