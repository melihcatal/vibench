import asyncio
import os
import azure.cognitiveservices.speech as speechsdk
from speech_client import create_speech_recognizer_with_settings

async def stream_with_language_and_punctuation(language='en-US', enable_punctuation=True):
    speech_recognizer = create_speech_recognizer_with_settings(language, enable_punctuation)
    if speech_recognizer is None:
        print("Speech recognizer could not be created. Check environment variables.")
        return

    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED ({}): {}'.format(language, evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt.reason, evt.error_details)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print(f"Say something in {language} with punctuation...\n(To test, try saying 'Hello world comma how are you question mark')")
    speech_recognizer.start_continuous_recognition()
    while not done:
        await asyncio.sleep(0.5)
    speech_recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    asyncio.run(stream_with_language_and_punctuation(language='en-US', enable_punctuation=True))
    # Example for another language (if supported by your Azure Speech region)
    # asyncio.run(stream_with_language_and_punctuation(language='es-ES', enable_punctuation=True))
