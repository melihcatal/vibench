import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config, create_push_audio_stream
from speech_models import TranscriptionResult, normalize_response
from queue import Queue
from threading import Thread

def stream_with_language(audio_data_stream, language_code, sample_rate_hz, enable_punctuation=True):
    speech_config = get_speech_config()
    speech_config.speech_recognition_language = language_code

    if enable_punctuation:
        # Azure Speech-to-Text automatically handles punctuation for most languages
        # when the language is set. No explicit separate setting for punctuation is usually needed.
        # If specific punctuation modes were required, it would be configured here.
        pass

    audio_input_stream = create_push_audio_stream(sample_rate_hz)
    audio_config = speechsdk.audio.AudioConfig(stream=audio_input_stream)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    results_queue = Queue()

    def handle_recognizing(e):
        normalized = normalize_response(e)
        if normalized:
            results_queue.put(normalized.to_dict())

    def handle_recognized(e):
        normalized = normalize_response(e)
        if normalized:
            results_queue.put(normalized.to_dict())

    def handle_session_stopped(e):
        results_queue.put(None)

    def handle_canceled(e):
        results_queue.put(RuntimeError(f"Speech recognition canceled: {e.reason}"))

    recognizer.recognizing.connect(handle_recognizing)
    recognizer.recognized.connect(handle_recognized)
    recognizer.session_stopped.connect(handle_session_stopped)
    recognizer.canceled.connect(handle_canceled)

    def feed_audio_data():
        try:
            for chunk in audio_data_stream:
                audio_input_stream.write(chunk)
        except Exception as ex:
            results_queue.put(ex)
        finally:
            audio_input_stream.close()

    recognizer.start_continuous_recognition_async().get()
    producer_thread = Thread(target=feed_audio_data, daemon=True)
    producer_thread.start()

    try:
        while True:
            result = results_queue.get()
            if result is None:
                break
            if isinstance(result, Exception):
                raise result
            yield result
    finally:
        recognizer.stop_continuous_recognition_async().get()
        audio_input_stream.close()
        producer_thread.join(timeout=1)
