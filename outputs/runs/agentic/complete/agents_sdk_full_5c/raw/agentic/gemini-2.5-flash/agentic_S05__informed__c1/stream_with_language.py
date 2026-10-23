import azure.cognitiveservices.speech as speechsdk
import os
import asyncio

from speech_client import get_speech_config, get_audio_config_from_microphone

async def stream_with_language_and_punctuation(language: str = "en-US", enable_punctuation: bool = True):
    speech_config = get_speech_config()
    speech_config.speech_recognition_language = language
    if enable_punctuation:
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText")

    audio_config = get_audio_config_from_microphone()

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        print("CLOSING on {}".format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED ({language}, Punctuation: {enable_punctuation}): {{}}".format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print("SESSION STARTED: {}".format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print("SESSION STOPPED {}".format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print("CANCELED: {} ({})".format(evt.reason, evt.error_details)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print(f"Speak into your microphone in {language} with punctuation {'enabled' if enable_punctuation else 'disabled'}.")
    speech_recognizer.start_continuous_recognition()
    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()
