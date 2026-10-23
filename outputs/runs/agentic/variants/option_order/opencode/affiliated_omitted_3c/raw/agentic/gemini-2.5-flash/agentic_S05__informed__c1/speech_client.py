import os
import azure.cognitiveservices.speech as speech_sdk


def create_speech_recognizer(
    language: str = "en-US",
):  # Using azure-cognitiveservices-speech SDK
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set."
        )

    speech_config = speech_sdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.speech_recognition_language = language
    return speech_config
