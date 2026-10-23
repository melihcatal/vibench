import asyncio
import azure.cognitiveservices.speech as speechsdk
from speech_client import SpeechClient
from speech_models import RecognitionResult


async def stream_audio_chunks(audio_stream_source):
    speech_client = SpeechClient()

    # Provider-specific: Azure AI Speech PushAudioInputStream for custom audio sources
    push_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)
    speech_recognizer = speech_client.get_speech_recognizer(audio_config)

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
        done.set()

    def session_stopped_cb(evt):
        print("Session stopped.")
        done.set()

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.canceled.connect(canceled_cb)
    speech_recognizer.session_stopped.connect(session_stopped_cb)

    speech_recognizer.start_continuous_recognition()

    async for chunk in audio_stream_source:
        push_stream.write(chunk)
    push_stream.close()

    await done.wait()
    speech_recognizer.stop_continuous_recognition()
