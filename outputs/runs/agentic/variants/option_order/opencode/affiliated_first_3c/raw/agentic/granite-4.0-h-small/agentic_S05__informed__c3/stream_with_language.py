# Azure Speech Streaming (service=Azure AI Speech streaming; sdk=azure-cognitiveservices-speech)
# AZURE_SPEECH_KEY, AZURE_SPEECH_REGION environment variables required

import os
import asyncio
from azure.cognitiveservices.speech import (
    AudioDataStream,
    SpeechConfig,
    SpeechRecognizer,
)


def create_recognizer():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    # Set language and enable punctuation
    speech_config.speech_recognition_language = "es-ES"  # Spanish example
    speech_config.set_property("enable_dictation", "true")
    recognizer = SpeechRecognizer(speech_config=speech_config)
    return recognizer


async def stream_with_language():
    recognizer = create_recognizer()
    # Simulated audio (replace with real mic)
    audio_input = AudioDataStream(None)  # placeholder
    async with recognizer.recognize_once_async(audio_input) as result:
        await result
        print("Recognized:", result.result.text)


asyncio.run(stream_with_language())
