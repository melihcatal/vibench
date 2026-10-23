import azure.cognitiveservices.speech as speechsdk
import asyncio
import os
from speech_client import get_speech_config, get_audio_config_from_microphone
from partial_results import PartialResultsHandler

async def stream_with_language_and_punctuation(language: str = "en-US", enable_punctuation: bool = True):
    speech_config = get_speech_config()
    audio_config = get_audio_config_from_microphone()

    speech_config.speech_recognition_language = language

    if enable_punctuation:
        # Enable dictation mode for automatic punctuation
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText")

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Setup partial results handling
    partial_results_handler = PartialResultsHandler()
    partial_results_handler.setup_recognizer_callbacks(speech_recognizer)

    print(f"Speak into your microphone in {language}...")

    done = False
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt.reason, evt.error_details)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition_async()

    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition_async()

if __name__ == "__main__":
    asyncio.run(stream_with_language_and_punctuation(language="es-ES"))
