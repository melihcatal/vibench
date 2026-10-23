import asyncio
from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config, get_audio_config, get_recognizer
from speech_models import SpeechRecognitionConfig, normalize_azure_result


async def stream_chunks(audio_chunks_async_source, config: SpeechRecognitionConfig):
    speech_config = get_speech_config()
    speech_config.speech_recognition_language = config.language_code

    push_stream = speechsdk.audio.PushAudioInputStream(speechsdk.audio.AudioStreamFormat(
        samples_per_second=config.sample_rate_hz, bits_per_sample=16, channels=1))
    
    audio_config = get_audio_config(push_stream)
    recognizer = get_recognizer(speech_config, audio_config)

    events_queue = Queue()

    def recognized_cb(e: speechsdk.SpeechRecognitionEventArgs):
        if e.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            events_queue.put(normalize_azure_result(e))

    def recognizing_cb(e: speechsdk.SpeechRecognitionEventArgs):
        if e.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            events_queue.put(normalize_azure_result(e))

    def session_stopped_cb(e: speechsdk.SessionEventArgs):
        events_queue.put(None)

    def canceled_cb(e: speechsdk.SpeechRecognitionCanceledEventArgs):
        events_queue.put(RuntimeError(f"Azure speech recognition canceled: {e.reason} {e.error_details}"))

    recognizer.recognized.connect(recognized_cb)
    recognizer.recognizing.connect(recognizing_cb)
    recognizer.session_stopped.connect(session_stopped_cb)
    recognizer.canceled.connect(canceled_cb)

    recognizer.start_continuous_recognition_async().get()

    async def feed_audio_chunks():
        try:
            async for chunk in audio_chunks_async_source:
                push_stream.write(chunk)
        except Exception as exc:
            events_queue.put(exc)
        finally:
            push_stream.close()

    audio_feeder_task = asyncio.create_task(feed_audio_chunks())

    try:
        while True:
            event = await asyncio.to_thread(events_queue.get, timeout=60)
            if event is None:
                break
            if isinstance(event, Exception):
                raise event
            yield event
    finally:
        await asyncio.to_thread(recognizer.stop_continuous_recognition_async().get)
        push_stream.close()
        await audio_feeder_task
