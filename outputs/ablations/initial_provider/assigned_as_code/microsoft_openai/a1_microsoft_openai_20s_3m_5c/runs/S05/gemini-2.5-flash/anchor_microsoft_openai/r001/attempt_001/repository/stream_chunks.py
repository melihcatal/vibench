import azure.cognitiveservices.speech as speechsdk
from queue import Queue
from threading import Thread
from speech_client import get_speech_config
from speech_models import StreamingRecognitionResult

def stream_chunks(audio_chunk_generator, language_code="en-US", sample_rate_hz=16000):
    speech_config = get_speech_config()
    speech_config.speech_recognition_language = language_code

    audio_format = speechsdk.audio.AudioStreamFormat(samples_per_second=sample_rate_hz, bits_per_sample=16, channels=1)
    push_stream = speechsdk.audio.PushAudioInputStream(audio_format)
    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)

    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    events_queue = Queue()

    def recognizing_handler(e):
        if e.result.text:
            events_queue.put(StreamingRecognitionResult(e.result.text, False).to_dict())

    def recognized_handler(e):
        if e.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            events_queue.put(StreamingRecognitionResult(e.result.text, True).to_dict())
        elif e.result.reason == speechsdk.ResultReason.NoMatch:
            pass # No speech could be recognized
        elif e.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = e.result.cancellation_details
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                events_queue.put(RuntimeError(f"Cancellation error: {cancellation_details.error_details}"))

    def session_stopped_handler(e):
        events_queue.put(None)

    recognizer.recognizing.connect(recognizing_handler)
    recognizer.recognized.connect(recognized_handler)
    recognizer.session_stopped.connect(session_stopped_handler)

    recognizer.start_continuous_recognition_async().get()

    def feed_audio():
        try:
            for chunk in audio_chunk_generator:
                push_stream.write(chunk)
        except Exception as exc:
            events_queue.put(exc)
        finally:
            push_stream.close()

    producer_thread = Thread(target=feed_audio, daemon=True)
    producer_thread.start()

    try:
        while True:
            event = events_queue.get(timeout=60)
            if event is None:
                break
            if isinstance(event, Exception):
                raise event
            yield event
    finally:
        recognizer.stop_continuous_recognition_async().get()
        push_stream.close()
        producer_thread.join(timeout=1)
