import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    return speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def get_speech_synthesizer():
    speech_config = get_speech_config()
    return speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
