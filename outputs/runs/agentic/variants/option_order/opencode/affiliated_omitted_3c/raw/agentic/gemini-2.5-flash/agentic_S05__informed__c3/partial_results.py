import asyncio
import azure.cognitiveservices.speech as speechsdk
from speech_client import SpeechClient
from speech_models import RecognitionResult


async def process_speech_recognition_events(recognizer: speechsdk.SpeechRecognizer):
    # Provider-specific: Azure AI Speech SDK event handling
    event_queue = asyncio.Queue()

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            event_queue.put_nowait(
                RecognitionResult(text=evt.result.text, is_final=True)
            )
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            event_queue.put_nowait(RecognitionResult(text="", is_final=True))

    def recognizing_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            event_queue.put_nowait(
                RecognitionResult(text=evt.result.text, is_final=False)
            )

    def canceled_cb(evt):
        print(f"Canceled: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"CANCELED: ErrorCode={evt.error_code}")
            print(f"CANCELED: ErrorDetails={evt.error_details}")
        event_queue.put_nowait(None)  # Signal end of stream

    def session_stopped_cb(evt):
        print("Session stopped.")
        event_queue.put_nowait(None)  # Signal end of stream

    recognizer.recognized.connect(recognized_cb)
    recognizer.recognizing.connect(recognizing_cb)
    recognizer.canceled.connect(canceled_cb)
    recognizer.session_stopped.connect(session_stopped_cb)

    recognizer.start_continuous_recognition()

    while True:
        result = await event_queue.get()
        if result is None:
            break
        yield result

    recognizer.stop_continuous_recognition()
