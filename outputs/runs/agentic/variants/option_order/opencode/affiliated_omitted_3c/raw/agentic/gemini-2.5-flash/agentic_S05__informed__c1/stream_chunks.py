import os
import azure.cognitiveservices.speech as speech_sdk
from speech_client import create_speech_recognizer
from speech_models import SpeechRecognitionResult
import queue
import threading


def stream_audio_chunks(
    audio_chunks_iterable, language: str = "en-US"
):  # Using azure-cognitiveservices-speech SDK
    speech_config = create_speech_recognizer(language)

    audio_format = speech_sdk.audio.AudioStreamFormat(
        samples_per_second=16000, bits_per_sample=16, channels=1
    )
    push_stream = speech_sdk.audio.PushAudioInputStream(audio_format)
    audio_config = speech_sdk.AudioConfig(stream=push_stream)
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
        elif evt.result.reason == speech_sdk.ResultReason.Canceled:
            pass

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

    speech_recognizer.start_continuous_recognition_async().get()

    for chunk in audio_chunks_iterable:
        push_stream.write(chunk)

    push_stream.close()

    while not done_event.is_set() or not results_queue.empty():
        try:
            result = results_queue.get(timeout=0.1)
            yield result
        except queue.Empty:
            continue

    speech_recognizer.stop_continuous_recognition_async().get()
