import azure.cognitiveservices.speech as speechsdk
import os
import asyncio

async def handle_partial_and_final_results(speech_config: speechsdk.SpeechConfig, audio_config: speechsdk.audio.AudioConfig):
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    def stop_cb(evt):
        print(f"CLOSING on {evt}")
        nonlocal done
        done = True

    def recognizing_cb(evt):
        if evt.result.text:
            print(f"PARTIAL: {evt.result.text}")

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"FINAL: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("NOMATCH: Speech could not be recognized.")

    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print(f"SESSION STARTED: {evt}"))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Say something to see partial and final results...")
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
        asyncio.run(handle_partial_and_final_results(speech_config, audio_config))
