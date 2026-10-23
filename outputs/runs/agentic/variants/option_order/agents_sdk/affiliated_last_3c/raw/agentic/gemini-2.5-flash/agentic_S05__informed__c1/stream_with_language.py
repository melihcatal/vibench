import azure.cognitiveservices.speech as speechsdk
import os
import asyncio

async def stream_with_language_and_punctuation(speech_config: speechsdk.SpeechConfig, audio_config: speechsdk.audio.AudioConfig, language: str = "en-US"):
    speech_config.speech_recognition_language = language
    speech_config.enable_punctuation_disambiguation(True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    def stop_cb(evt):
        print(f"CLOSING on {evt}")
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED ({language}): {evt.result.text}"))
    speech_recognizer.session_started.connect(lambda evt: print(f"SESSION STARTED: {evt}"))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print(f"Say something in {language} to see punctuation...")
    speech_recognizer.start_continuous_recognition()

    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        print("Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")
    else:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioConfig(use_microphone=True)
        
        # Example with US English
        asyncio.run(stream_with_language_and_punctuation(speech_config, audio_config, "en-US"))

        # Example with British English (if supported by the service and region)
        # Note: Depending on the Azure region, some languages might have better support than others.
        # To run this, you'd likely need to re-initialize speech_config or pass a new one if settings are truly global.
        # For simplicity, we are reusing the config for demonstration.
        # print("\nNow trying with British English...")
        # asyncio.run(stream_with_language_and_punctuation(speech_config, audio_config, "en-GB"))
