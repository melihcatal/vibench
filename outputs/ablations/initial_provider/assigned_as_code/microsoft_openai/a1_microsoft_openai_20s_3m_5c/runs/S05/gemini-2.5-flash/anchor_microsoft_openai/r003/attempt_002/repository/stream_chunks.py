from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config, create_push_audio_stream
from speech_models import TranscriptionResult, normalize_response

async def stream_chunks(audio_chunk_generator, language_code, sample_rate_hz, config=None):
    speech_config = get_speech_config()
    speech_config.speech_recognition_language = language_code
    audio_stream = create_push_audio_stream(sample_rate_hz)
    audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    events_queue = Queue()

    def recognizing_handler(e):
        normalized_result = normalize_response(e)
        if normalized_result:
            events_queue.put(normalized_result.to_dict())

    def recognized_handler(e):
        normalized_result = normalize_response(e)
        if normalized_result:
            events_queue.put(normalized_result.to_dict())

    def session_stopped_handler(e):
        events_queue.put(None)

    def canceled_handler(e):
        events_queue.put(RuntimeError(f"Azure speech recognition canceled: {e.reason}"))

    recognizer.recognizing.connect(recognizing_handler)
    recognizer.recognized.connect(recognized_handler)
    recognizer.session_stopped.connect(session_stopped_handler)
    recognizer.canceled.connect(canceled_handler)

    def feed_audio():
        try:
            for chunk in audio_chunk_generator:
                audio_stream.write(chunk)
        except Exception as exc:
            events_queue.put(exc)
        finally:
            audio_stream.close()

    recognizer.start_continuous_recognition_async().get()
    producer_thread = Thread(target=feed_audio, daemon=True)
    producer_thread.start()

    try:
        while True:
            event = events_queue.get()
            if event is None:
                break
            if isinstance(event, Exception):
                raise event
            yield event
    finally:
        recognizer.stop_continuous_recognition_async().get()
        audio_stream.close()
        producer_thread.join(timeout=1)
