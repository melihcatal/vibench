import os
import asyncio
from typing import AsyncGenerator, Dict, Any
from deepgram import Deepgram
import boto3
from botocore.exceptions import ClientError


class LiveCaptionTranslator:
    def __init__(self, source_lang: str = "en", target_lang: str = "es"):
        self.source_lang = source_lang
        self.target_lang = target_lang

        self.dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

        self.translate_client = boto3.client(
            "translate",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    async def translate_caption(
        self, caption_text: str, is_final: bool = True
    ) -> Dict[str, Any]:
        if not caption_text.strip():
            return {
                "original": "",
                "translated": "",
                "source_lang": self.source_lang,
                "target_lang": self.target_lang,
                "is_final": is_final,
            }

        try:
            response = self.translate_client.translate_text(
                Text=caption_text,
                SourceLanguageCode=self.source_lang,
                TargetLanguageCode=self.target_lang,
            )

            return {
                "original": caption_text,
                "translated": response["TranslatedText"],
                "source_lang": response.get("SourceLanguageCode", self.source_lang),
                "target_lang": self.target_lang,
                "is_final": is_final,
            }

        except ClientError as e:
            print(f"Translation error: {e}")
            return {
                "original": caption_text,
                "translated": caption_text,
                "source_lang": self.source_lang,
                "target_lang": self.target_lang,
                "is_final": is_final,
                "error": str(e),
            }

    async def stream_and_translate(
        self, audio_source
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async with self.dg_client.transcription.live(
            {
                "model": "nova-2",
                "language": self.source_lang if self.source_lang != "en" else "en-US",
                "interim_results": True,
                "smart_format": True,
                "encoding": "linear16",
                "sample_rate": 16000,
                "channels": 1,
            }
        ) as connection:

            async def send_audio():
                async for chunk in audio_source:
                    await connection.send(chunk)

            async def process_transcripts():
                async for message in connection:
                    if "channel" in message:
                        for alternative in message["channel"]["alternatives"]:
                            if "transcript" in alternative:
                                transcript = alternative["transcript"]
                                if transcript:
                                    is_final = message.get("is_final", False)
                                    translation = await self.translate_caption(
                                        transcript, is_final
                                    )
                                    yield translation

            send_task = asyncio.create_task(send_audio())

            try:
                async for translation in process_transcripts():
                    yield translation
            finally:
                send_task.cancel()
                try:
                    await send_task
                except asyncio.CancelledError:
                    pass


async def example_translation():
    translator = LiveCaptionTranslator(source_lang="en", target_lang="es")

    class TestAudio:
        async def __aiter__(self):
            for i in range(5):
                yield b"\x00" * 1024
                await asyncio.sleep(0.1)

    audio_source = TestAudio()

    print("Streaming and translating captions...")
    async for result in translator.stream_and_translate(audio_source):
        status = "FINAL" if result["is_final"] else "INTERIM"
        print(f"\n{status} Original: {result['original']}")
        print(f"{status} Translated ({result['target_lang']}): {result['translated']}")


if __name__ == "__main__":
    asyncio.run(example_translation())
