import asyncio
import aiohttp
import json
from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioConfig,
    SpeechRecognizer,
    ResultReason,
)
from azure.cognitiveservices.speech.audio import PushAudioInputStream


async def stream_audio_chunks(audio_source_url):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "en-US"
    speech_config.request_word_level_timestamps()

    push_stream = PushAudioInputStream()
    audio_config = AudioConfig(stream=push_stream)

    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    transcript_queue = asyncio.Queue()

    def recognized_handler(evt):
        if evt.result.reason == ResultReason.RecognizedSpeech:
            asyncio.create_task(
                transcript_queue.put(
                    {
                        "text": evt.result.text,
                        "is_final": True,
                        "duration": evt.result.duration.total_seconds()
                        if evt.result.duration
                        else None,
                    }
                )
            )

    def recognizing_handler(evt):
        if evt.result.reason == ResultReason.RecognizingSpeech:
            asyncio.create_task(
                transcript_queue.put(
                    {
                        "text": evt.result.text,
                        "is_final": False,
                        "duration": evt.result.duration.total_seconds()
                        if evt.result.duration
                        else None,
                    }
                )
            )

    recognizer.recognized.connect(recognized_handler)
    recognizer.recognizing.connect(recognizing_handler)

    recognizer.start_continuous_recognition()

    async with aiohttp.ClientSession() as session:
        async with session.get(audio_source_url) as response:
            if response.status != 200:
                raise ValueError(f"Failed to fetch audio from {audio_source_url}")

            async for chunk in response.content.iter_chunked(4096):
                if chunk:
                    push_stream.write(chunk)
                    await asyncio.sleep(0)

                try:
                    while not transcript_queue.empty():
                        transcript = await transcript_queue.get()
                        yield transcript
                except asyncio.QueueEmpty:
                    pass

    recognizer.stop_continuous_recognition()
    push_stream.close()

    while not transcript_queue.empty():
        transcript = await transcript_queue.get()
        yield transcript


async def stream_from_async_generator(audio_generator):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "en-US"

    push_stream = PushAudioInputStream()
    audio_config = AudioConfig(stream=push_stream)

    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    transcript_queue = asyncio.Queue()

    def result_handler(evt):
        if evt.result.reason == ResultReason.RecognizedSpeech:
            asyncio.create_task(
                transcript_queue.put({"text": evt.result.text, "is_final": True})
            )
        elif evt.result.reason == ResultReason.RecognizingSpeech:
            asyncio.create_task(
                transcript_queue.put({"text": evt.result.text, "is_final": False})
            )

    recognizer.recognized.connect(result_handler)
    recognizer.recognizing.connect(result_handler)

    recognizer.start_continuous_recognition()

    async for audio_chunk in audio_generator:
        if audio_chunk:
            push_stream.write(audio_chunk)
            await asyncio.sleep(0)

        try:
            while not transcript_queue.empty():
                transcript = await transcript_queue.get()
                yield transcript
        except asyncio.QueueEmpty:
            pass

    recognizer.stop_continuous_recognition()
    push_stream.close()

    while not transcript_queue.empty():
        transcript = await transcript_queue.get()
        yield transcript


if __name__ == "__main__":
    import os

    async def test_generator():
        for i in range(10):
            yield b"\x00" * 1024
            await asyncio.sleep(0.1)

    async def main():
        async for transcript in stream_from_async_generator(test_generator()):
            print(f"Transcript: {transcript}")

    asyncio.run(main())
