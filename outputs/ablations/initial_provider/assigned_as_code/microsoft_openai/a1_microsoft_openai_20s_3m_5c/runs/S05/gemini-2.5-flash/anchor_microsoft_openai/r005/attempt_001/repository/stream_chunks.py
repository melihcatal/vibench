import asyncio
from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk
from speech_client import create_speech_recognizer
from speech_models import SpeechConfig, normalize_azure_speech_event


async def stream_chunks(audio_chunks_async_iterable, config: SpeechConfig):
    speech_config = speechsdk.SpeechConfig(subscription=config.api_key, region=config.region)
    speech_config.speech_recognition_language = config.language_code

    audio_format = speechsdk.audio.AudioStreamFormat(
        samples_per_second=config.sample_rate_hz, bits_per_sample=16, channels=1)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
    
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=speechsdk.audio.AudioConfig(stream=stream))

    events = Queue()
    recognizer.recognizing.connect(lambda e: events.put(normalize_azure_speech_event(e)))
    recognizer.recognized.connect(lambda e: events.put(normalize_azure_speech_event(e) if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None))
    recognizer.session_stopped.connect(lambda e: events.put(None))
    recognizer.canceled.connect(lambda e: events.put(RuntimeError('Azure speech recognition canceled')))

    async def feed_audio():
        try:
            async for chunk in audio_chunks_async_iterable:
                stream.write(chunk)
        except Exception as exc:
            events.put(exc)
        finally:
            stream.close()
    
    # Start the recognition asynchronously
    await asyncio.to_thread(recognizer.start_continuous_recognition_async().get)
    producer = asyncio.create_task(feed_audio())

    try:
        while True:
            event = await asyncio.to_thread(events.get, timeout=60)
            if event is None:
                break
            if isinstance(event, Exception):
                raise event
            yield event
    finally:
        await asyncio.to_thread(recognizer.stop_continuous_recognition_async().get)
        stream.close()
        await producer # Ensure producer task is awaited
