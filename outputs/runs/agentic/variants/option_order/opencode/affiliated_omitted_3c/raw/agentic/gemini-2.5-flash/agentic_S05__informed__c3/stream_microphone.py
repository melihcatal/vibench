import asyncio
import azure.cognitiveservices.speech as speechsdk
from speech_client import SpeechClient
from speech_models import RecognitionResult


async def stream_microphone_audio():
    speech_client = SpeechClient()
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_client.get_speech_recognizer(audio_config)

    # Provider-specific: Azure AI Speech SDK for streaming
    done = asyncio.Event()

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Final: {evt.result.text}")
            yield RecognitionResult(text=evt.result.text, is_final=True)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")

    def recognizing_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            print(f"Interim: {evt.result.text}")
            yield RecognitionResult(text=evt.result.text, is_final=False)

    def canceled_cb(evt):
        print(f"Canceled: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"CANCELED: ErrorCode={evt.error_code}")
            print(f"CANCELED: ErrorDetails={evt.error_details}")
            print(f"CANCELED: Did you set the speech resource key and region values?")
        done.set()

    def session_stopped_cb(evt):
        print("Session stopped.")
        done.set()

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.canceled.connect(canceled_cb)
    speech_recognizer.session_stopped.connect(session_stopped_cb)

    print("Speak into your microphone.")
    speech_recognizer.start_continuous_recognition()
    await done.wait()
    speech_recognizer.stop_continuous_recognition()
