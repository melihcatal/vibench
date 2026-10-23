import asyncio

import azure.cognitiveservices.speech as speechsdk

from speech_client import make_azure_speech_config
from speech_models import transcript_from_result


async def stream_chunks(audio_source):
    speech_config = make_azure_speech_config(speechsdk)
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.AudioConfig(stream=stream)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    results = asyncio.Queue()

    def on_recognized(evt):
        if evt.result.text:
            results.put_nowait(
                transcript_from_result(
                    evt.result.text,
                    final=True,
                    language=speech_config.speech_recognition_language,
                )
            )

    recognizer.recognized.connect(on_recognized)
    recognizer.start_continuous_recognition()
    try:
        async for chunk in audio_source:
            stream.write(chunk)
            while not results.empty():
                yield await results.get()
        stream.close()
        await asyncio.sleep(0)
        while not results.empty():
            yield await results.get()
    finally:
        recognizer.stop_continuous_recognition()
