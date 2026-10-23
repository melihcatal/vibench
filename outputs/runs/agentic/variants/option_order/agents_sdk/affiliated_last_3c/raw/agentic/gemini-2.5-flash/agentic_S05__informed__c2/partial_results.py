import asyncio
import os
import azure.cognitiveservices.speech as speechsdk
from speech_client import create_speech_recognizer

async def handle_streaming_recognition_events():
    speech_recognizer = create_speech_recognizer()
    if speech_recognizer is None:
        print("Speech recognizer could not be created. Check environment variables.")
        return

    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"FINAL RESULT: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("NOMATCH: Speech could not be recognized.")

    def recognizing_cb(evt):
        print(f"PARTIAL RESULT: {evt.result.text}")

    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt.reason, evt.error_details)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Say something to see partial and final results...")
    speech_recognizer.start_continuous_recognition()
    while not done:
        await asyncio.sleep(0.5)
    speech_recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    asyncio.run(handle_streaming_recognition_events())
