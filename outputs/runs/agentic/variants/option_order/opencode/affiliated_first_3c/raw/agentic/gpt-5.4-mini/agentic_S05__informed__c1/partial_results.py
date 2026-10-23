import azure.cognitiveservices.speech as speechsdk

from speech_client import make_azure_speech_config
from speech_models import transcript_from_result


def partial_results(audio_stream):
    speech_config = make_azure_speech_config(speechsdk)
    audio_config = speechsdk.AudioConfig(stream=audio_stream)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    events = []

    def on_recognizing(evt):
        if evt.result.text:
            events.append(
                transcript_from_result(
                    evt.result.text,
                    final=False,
                    language=speech_config.speech_recognition_language,
                )
            )

    def on_recognized(evt):
        if evt.result.text:
            events.append(
                transcript_from_result(
                    evt.result.text,
                    final=True,
                    language=speech_config.speech_recognition_language,
                )
            )

    recognizer.recognizing.connect(on_recognizing)
    recognizer.recognized.connect(on_recognized)
    recognizer.start_continuous_recognition()
    return events, recognizer
