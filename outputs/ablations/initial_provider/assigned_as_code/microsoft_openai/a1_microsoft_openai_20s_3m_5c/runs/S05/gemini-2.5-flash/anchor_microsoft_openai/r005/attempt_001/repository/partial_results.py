import azure.cognitiveservices.speech as speechsdk
from queue import Queue
from threading import Thread
from speech_models import normalize_azure_speech_event

def handle_partial_results(recognizer: speechsdk.SpeechRecognizer):
    events = Queue()

    def recognizing_handler(e: speechsdk.SpeechRecognitionEventArgs):
        events.put(normalize_azure_speech_event(e))

    def recognized_handler(e: speechsdk.SpeechRecognitionEventArgs):
        if e.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            events.put(normalize_azure_speech_event(e))

    def session_stopped_handler(e: speechsdk.SessionEventArgs):
        events.put(None)

    def canceled_handler(e: speechsdk.SpeechRecognitionCanceledEventArgs):
        events.put(RuntimeError(f"Azure speech recognition canceled: {e.reason}"))

    recognizer.recognizing.connect(recognizing_handler)
    recognizer.recognized.connect(recognized_handler)
    recognizer.session_stopped.connect(session_stopped_handler)
    recognizer.canceled.connect(canceled_handler)

    # Start continuous recognition if not already started by the caller
    # This assumes the recognizer is already configured with an audio input
    # For this specific file, we will assume the recognizer is already set up to receive audio
    
    try:
        while True:
            event = events.get(timeout=60)
            if event is None:
                break
            if isinstance(event, Exception):
                raise event
            yield event
    finally:
        # Disconnect handlers to prevent resource leaks if the recognizer is reused
        recognizer.recognizing.disconnect(recognizing_handler)
        recognizer.recognized.disconnect(recognized_handler)
        recognizer.session_stopped.disconnect(session_stopped_handler)
        recognizer.canceled.disconnect(canceled_handler)
