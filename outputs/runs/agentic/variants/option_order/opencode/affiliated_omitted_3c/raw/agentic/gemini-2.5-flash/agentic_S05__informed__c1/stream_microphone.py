import os
import azure.cognitiveservices.speech as speech_sdk
from speech_client import create_speech_recognizer
from speech_models import SpeechRecognitionResult
import queue
import threading


def stream_microphone_audio(
    language: str = "en-US",
):  # Using azure-cognitiveservices-speech SDK
    speech_config = create_speech_recognizer(language)
    audio_config = speech_sdk.AudioConfig(use_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    results_queue = queue.Queue()
    done_event = threading.Event()

    def recognized_cb(evt: speech_sdk.SpeechRecognitionEventArgs):
        if evt.result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            results_queue.put(
                SpeechRecognitionResult(
                    text=evt.result.text, is_final=True, language=language
                )
            )
        elif evt.result.reason == speech_sdk.ResultReason.NoMatch:
            pass  # No speech could be recognized.
        elif evt.result.reason == speech_sdk.ResultReason.Canceled:
            pass  # Canceled: Reason={evt.result.cancellation_details.reason}

    def recognizing_cb(evt: speech_sdk.SpeechRecognitionEventArgs):
        if evt.result.reason == speech_sdk.ResultReason.RecognizingSpeech:
            results_queue.put(
                SpeechRecognitionResult(
                    text=evt.result.text, is_final=False, language=language
                )
            )

    def stopped_cb(evt: speech_sdk.SessionEventArgs):
        done_event.set()

    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stopped_cb)
    speech_recognizer.canceled.connect(stopped_cb)

    speech_recognizer.start_continuous_recognition()

    while not done_event.is_set() or not results_queue.empty():
        try:
            result = results_queue.get(timeout=0.1)
            yield result
        except queue.Empty:
            continue

    speech_recognizer.stop_continuous_recognition()
