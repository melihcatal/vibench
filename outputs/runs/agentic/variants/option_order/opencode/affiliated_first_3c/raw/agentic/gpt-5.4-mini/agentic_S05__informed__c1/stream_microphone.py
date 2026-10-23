import azure.cognitiveservices.speech as speechsdk

from speech_client import make_azure_speech_config
from speech_models import transcript_from_result


def stream_microphone():
    speech_config = make_azure_speech_config(speechsdk)
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    queue = []

    def on_recognizing(evt):
        if evt.result.text:
            queue.append(
                transcript_from_result(
                    evt.result.text,
                    final=False,
                    language=speech_config.speech_recognition_language,
                )
            )

    recognizer.recognizing.connect(on_recognizing)
    recognizer.start_continuous_recognition()
    try:
        while True:
            while queue:
                yield queue.pop(0)
    finally:
        recognizer.stop_continuous_recognition()
