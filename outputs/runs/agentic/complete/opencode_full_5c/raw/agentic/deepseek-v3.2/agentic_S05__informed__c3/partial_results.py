import asyncio
from typing import AsyncGenerator, Dict, Any
from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioConfig,
    SpeechRecognizer,
    ResultReason,
)
from azure.cognitiveservices.speech.audio import PushAudioInputStream


class StreamingRecognitionHandler:
    def __init__(self):
        self.partial_results = []
        self.final_results = []
        self.current_partial = ""

    def handle_partial(self, text: str):
        self.current_partial = text
        self.partial_results.append(
            {
                "text": text,
                "is_final": False,
                "timestamp": asyncio.get_event_loop().time(),
            }
        )
        return self.current_partial

    def handle_final(self, text: str):
        self.final_results.append(
            {
                "text": text,
                "is_final": True,
                "timestamp": asyncio.get_event_loop().time(),
            }
        )
        self.current_partial = ""
        return text

    def get_latest_partial(self) -> str:
        return self.current_partial

    def get_all_finals(self) -> list:
        return self.final_results.copy()


async def handle_streaming_recognition(
    audio_stream: AsyncGenerator[bytes, None],
) -> AsyncGenerator[Dict[str, Any], None]:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "en-US"
    speech_config.enable_dictation()

    push_stream = PushAudioInputStream()
    audio_config = AudioConfig(stream=push_stream)

    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    handler = StreamingRecognitionHandler()

    def recognized_callback(evt):
        if evt.result.reason == ResultReason.RecognizedSpeech:
            result = {
                "text": evt.result.text,
                "is_final": True,
                "confidence": evt.result.confidence,
                "duration": evt.result.duration.total_seconds()
                if evt.result.duration
                else None,
                "offset": evt.result.offset / 10000000 if evt.result.offset else None,
            }
            asyncio.create_task(_result_queue.put(result))
            handler.handle_final(evt.result.text)

    def recognizing_callback(evt):
        if evt.result.reason == ResultReason.RecognizingSpeech:
            result = {
                "text": evt.result.text,
                "is_final": False,
                "confidence": evt.result.confidence,
                "duration": evt.result.duration.total_seconds()
                if evt.result.duration
                else None,
                "offset": evt.result.offset / 10000000 if evt.result.offset else None,
            }
            asyncio.create_task(_result_queue.put(result))
            handler.handle_partial(evt.result.text)

    _result_queue = asyncio.Queue()

    recognizer.recognized.connect(recognized_callback)
    recognizer.recognizing.connect(recognizing_callback)

    recognizer.start_continuous_recognition()

    async def audio_producer():
        async for chunk in audio_stream:
            if chunk:
                push_stream.write(chunk)
            await asyncio.sleep(0)

        await asyncio.sleep(1)
        recognizer.stop_continuous_recognition()
        push_stream.close()

    producer_task = asyncio.create_task(audio_producer())

    try:
        while True:
            try:
                result = await asyncio.wait_for(_result_queue.get(), timeout=5.0)
                yield result
            except asyncio.TimeoutError:
                if producer_task.done():
                    break
                continue
    finally:
        if not producer_task.done():
            producer_task.cancel()
            try:
                await producer_task
            except asyncio.CancelledError:
                pass

        recognizer.stop_continuous_recognition()
        push_stream.close()


async def process_partial_events(event_stream: AsyncGenerator[Dict[str, Any], None]):
    buffer = []
    current_sentence = ""

    async for event in event_stream:
        if event["is_final"]:
            if buffer:
                for buffered in buffer:
                    yield buffered
                buffer.clear()

            yield event

            if current_sentence:
                current_sentence = ""
        else:
            buffer.append(event)

            partial_text = event["text"]
            if len(partial_text) > len(current_sentence):
                current_sentence = partial_text

            if len(buffer) > 5:
                oldest = buffer.pop(0)
                if oldest["text"] in current_sentence:
                    current_sentence = current_sentence.replace(
                        oldest["text"], "", 1
                    ).strip()

    for remaining in buffer:
        yield remaining


if __name__ == "__main__":
    import os

    async def mock_audio_stream():
        for i in range(5):
            yield b"\x00" * 2048
            await asyncio.sleep(0.5)

    async def main():
        async for result in handle_streaming_recognition(mock_audio_stream()):
            print(f"Result: {result}")

    asyncio.run(main())
