import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig


def poll_transcription(job_id):
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    recognizer = SpeechRecognizer(speech_config=speech_config)
    result = recognizer.get_transcription_result(job_id)
    return result.text
