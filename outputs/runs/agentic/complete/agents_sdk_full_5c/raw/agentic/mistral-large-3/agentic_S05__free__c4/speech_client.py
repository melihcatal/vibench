import os
from openai import AsyncOpenAI

class SpeechClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def streaming_recognize(self, config: dict, audio_input_queue):
        if audio_input_queue is None:
            audio_input_queue = asyncio.Queue()

        async def audio_generator():
            while True:
                chunk = await audio_input_queue.get()
                if chunk is None:
                    break
                yield chunk

        stream = await self.client.audio.transcriptions.create(
            model=config["model"],
            language=config.get("language"),
            response_format=config.get("response_format", "text"),
            file=audio_generator(),
        )
        return stream

def get_speech_client():
    return SpeechClient()