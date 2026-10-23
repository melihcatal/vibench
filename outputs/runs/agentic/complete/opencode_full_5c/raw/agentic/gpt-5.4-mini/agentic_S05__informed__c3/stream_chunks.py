import asyncio

import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config


async def stream_chunks(chunk_source):
    cfg = load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    audio_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    async for chunk in chunk_source:
        audio_stream.write(chunk)
        await asyncio.sleep(0)
        yield recognizer.recognize_once_async().get().text
