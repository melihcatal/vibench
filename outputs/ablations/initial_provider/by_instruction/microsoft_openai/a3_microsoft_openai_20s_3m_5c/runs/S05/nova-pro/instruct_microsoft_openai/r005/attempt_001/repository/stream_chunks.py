import asyncio
import azure.cognitiveservices.speech as speechsdk

async def stream_chunks():
    speech_config = speechsdk.SpeechConfig(subscription="YOUR_SUBSCRIPTION_KEY", region="YOUR_SERVICE_REGION")
    audio_config = speechsdk.audio.AudioConfig(filename="YOUR_AUDIO_FILE")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        nonlocal done
        done = True

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    result = speech_recognizer.start_continuous_recognition_async()
    while not done:
        await asyncio.sleep(0.1)
    await result