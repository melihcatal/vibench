import azure.cognitiveservices.speech as speechsdk
import asyncio
from speech_client import get_speech_config, get_audio_config_from_microphone

async def stream_microphone_audio():
    speech_config = get_speech_config()
    audio_config = get_audio_config_from_microphone()

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone...")

    done = False
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt.reason, evt.error_details)))

    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition_async()

    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition_async()

if __name__ == "__main__":
    asyncio.run(stream_microphone_audio())
