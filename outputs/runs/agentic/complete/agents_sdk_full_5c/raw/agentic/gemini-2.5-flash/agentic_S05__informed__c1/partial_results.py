import azure.cognitiveservices.speech as speechsdk
import os
import asyncio

from speech_client import get_speech_recognizer

async def handle_partial_and_final_results():
    speech_recognizer = get_speech_recognizer()

    done = False

    def stop_cb(evt):
        print("CLOSING on {}".format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognizing.connect(lambda evt: print("RECOGNIZING: {}".format(evt.result.text)))
    speech_recognizer.recognized.connect(lambda evt: print("RECOGNIZED (FINAL): {}".format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print("SESSION STARTED: {}".format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print("SESSION STOPPED {}".format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print("CANCELED: {} ({})".format(evt.reason, evt.error_details)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Speak into your microphone for partial and final results.")
    speech_recognizer.start_continuous_recognition()
    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()
