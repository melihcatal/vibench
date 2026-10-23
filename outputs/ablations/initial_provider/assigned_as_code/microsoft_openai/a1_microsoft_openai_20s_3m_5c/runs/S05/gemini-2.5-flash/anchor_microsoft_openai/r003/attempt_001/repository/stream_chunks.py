import asyncio
from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config, get_push_audio_input_stream, get_speech_recognizer
from speech_models import normalize_azure_speech_result


async def stream_chunks(audio_chunks_async_iter, config=None):
    config = config or {}
    speech_config = get_speech_config(api_key=config['api_key'], region=config['region'],
                                      language_code=config.get('language_code', "en-US"))
    
    # Assuming fixed audio format for chunks, adjust if needed
    stream = get_push_audio_input_stream(sample_rate_hz=config.get('sample_rate_hz', 16000))
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    recognizer = get_speech_recognizer(speech_config=speech_config, audio_config=audio_config)
    
    events = Queue()
    recognizer.recognizing.connect(lambda e: events.put(normalize_azure_speech_result(e, is_final=False)))
    recognizer.recognized.connect(lambda e:
                                  events.put(normalize_azure_speech_result(e, is_final=True))
                                  if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None)
    recognizer.session_stopped.connect(lambda e: events.put(None))
    recognizer.canceled.connect(lambda e: events.put(RuntimeError(f'Azure speech recognition canceled: {e.reason}')))

    async def feed_async():
        try:
            async for chunk in audio_chunks_async_iter:
                stream.write(chunk)
        except Exception as exc:
            events.put(exc)
        finally:
            stream.close()
    
    # Start the recognition asynchronously
    await recognizer.start_continuous_recognition_async()
    
    # Run the feed_async in a separate thread to not block the event loop
    loop = asyncio.get_event_loop()
    producer_task = loop.run_in_executor(None, lambda: asyncio.run(feed_async()))
    
    try:
        while True:
            # Use a non-blocking way to get from queue or check for an event that signals termination
            # For simplicity, we'll use a blocking get with a timeout for now, similar to stream_microphone
            # In a real async app, you might use an async queue or more sophisticated signaling.
            event = events.get(timeout=60)
            if event is None:
                break
            if isinstance(event, Exception):
                raise event
            yield event
    finally:
        await recognizer.stop_continuous_recognition_async()
        stream.close()
        # Wait for the producer task to finish if it's still running
        await asyncio.wait([producer_task], timeout=1.0)
