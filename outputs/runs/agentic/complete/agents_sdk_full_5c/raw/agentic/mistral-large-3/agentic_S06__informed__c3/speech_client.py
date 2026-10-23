import os
import azure.cognitiveservices.speech as speechsdk


def get_speech_config() -> speechsdk.SpeechConfig:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set in environment variables."
        )
    return speechsdk.SpeechConfig(subscription=speech_key, region=service_region)