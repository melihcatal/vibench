import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config, get_audio_config, get_recognizer
from speech_models import SpeechRecognitionConfig, normalize_azure_result
from queue import Queue
from threading import Thread


def start_streaming_with_language(audio_chunks_iterable, language_code: str, enable_automatic_punctuation: bool = False):
    speech_config = get_speech_config()
    speech_config.speech_recognition_language = language_code
    
    # Azure SDK automatically handles punctuation based on language code to a certain extent.
    # For explicit control, you might need to use other methods or rely on model capabilities.
    # For simplicity, we assume setting language code implies relevant punctuation handling for Azure.
    
    push_stream = speechsdk.audio.PushAudioInputStream(speechsdk.audio.AudioStreamFormat(
        samples_per_second=16000, bits_per_sample=16, channels=1))
    
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

    def feed_audio_chunks():
        try:
            for chunk in audio_chunks_iterable:
                push_stream.write(chunk)
        except Exception as exc:
            events_queue.put(exc)
        finally:
            push_stream.close()

    audio_feeder_thread = Thread(target=feed_audio_chunks, daemon=True)
    audio_feeder_thread.start()

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
        audio_feeder_thread.join(timeout=1)
