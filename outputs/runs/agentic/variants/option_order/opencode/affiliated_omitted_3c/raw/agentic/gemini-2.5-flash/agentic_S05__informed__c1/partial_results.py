import os
import azure.cognitiveservices.speech as speech_sdk
from speech_client import create_speech_recognizer
from speech_models import SpeechRecognitionResult


def handle_streaming_recognition(
    audio_source, on_partial_result, on_final_result, language: str = "en-US"
):  # Using azure-cognitiveservices-speech SDK
    speech_config = create_speech_recognizer(language)

    if hasattr(audio_source, "read"):  # Assume it's a file-like object or similar
        audio_config = speech_sdk.AudioConfig(stream=audio_source)
    else:  # Assume microphone
        audio_config = speech_sdk.AudioConfig(use_microphone=True)

    speech_recognizer = speech_sdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    done = False

    def recognized_cb(evt: speech_sdk.SpeechRecognitionEventArgs):
        nonlocal done
        if evt.result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            on_final_result(
                SpeechRecognitionResult(
                    text=evt.result.text, is_final=True, language=language
                )
            )
        elif evt.result.reason == speech_sdk.ResultReason.NoMatch:
            pass
        elif evt.result.reason == speech_sdk.ResultReason.Canceled:
            done = True

    def recognizing_cb(evt: speech_sdk.SpeechRecognitionEventArgs):
        if evt.result.reason == speech_sdk.ResultReason.RecognizingSpeech:
            on_partial_result(
                SpeechRecognitionResult(
                    text=evt.result.text, is_final=False, language=language
                )
            )

    def stopped_cb(evt: speech_sdk.SessionEventArgs):
        nonlocal done
        done = True

    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stopped_cb)
    speech_recognizer.canceled.connect(stopped_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        import time

        time.sleep(0.1)
    speech_recognizer.stop_continuous_recognition()
