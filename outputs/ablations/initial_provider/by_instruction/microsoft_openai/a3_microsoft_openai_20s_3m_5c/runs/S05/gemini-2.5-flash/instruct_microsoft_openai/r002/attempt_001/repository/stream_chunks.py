import azure.cognitiveservices.speech as speechsdk
import asyncio
import os

async def stream_audio_chunks(audio_chunk_generator):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "en-US"

    audio_input_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.AudioConfig(stream=audio_input_stream)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result_queue = asyncio.Queue()

    def recognizing_cb(evt):
        result_queue.put_nowait({"type": "recognizing", "text": evt.result.text})

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            result_queue.put_nowait({"type": "recognized", "text": evt.result.text})
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            result_queue.put_nowait({"type": "recognized", "text": ""})

    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)

    speech_recognizer.start_continuous_recognition_async().get()

    try:
        async for chunk in audio_chunk_generator:
            audio_input_stream.write(chunk)
        audio_input_stream.close()

        while True:
            result = await result_queue.get()
            yield result

    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        speech_recognizer.stop_continuous_recognition_async().get()
