import asyncio
import azure.cognitiveservices.speech as speechsdk
from typing import AsyncGenerator, Tuple
from speech_client import get_speech_config

async def partial_results() -> AsyncGenerator[Tuple[str, str], None]:
    config = get_speech_config('azure')
    speech_key = config['key']
    speech_region = config['region']
    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY or AZURE_SPEECH_REGION not set")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    event_queue: asyncio.Queue[Tuple[str, str]] = asyncio.Queue()

    def on_recognizing(evt):
        asyncio.create_task(event_queue.put(('partial', evt.result.text)))

    def on_recognized(evt):
        asyncio.create_task(event_queue.put(('final', evt.result.text)))

    recognizer.recognizing.connect(on_recognizing)
    recognizer.recognized.connect(on_recognized)

    recognizer.start_continuous_recognition()

    try:
        while True:
            yield await event_queue.get()
    finally:
        recognizer.stop_continuous_recognition()