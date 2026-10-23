import asyncio
from typing import Optional, AsyncGenerator
from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioConfig,
    SpeechRecognizer,
    ResultReason,
    ProfanityOption,
    SpeechSynthesisOutputFormat,
)
from azure.cognitiveservices.speech.audio import PushAudioInputStream


async def start_streaming_recognizer(
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    profanity_filter: bool = True,
    word_level_timestamps: bool = False,
    audio_stream: Optional[AsyncGenerator[bytes, None]] = None,
) -> AsyncGenerator[dict, None]:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = language_code

    if enable_punctuation:
        speech_config.set_property(
            property_id="SpeechServiceResponse_RequestPunctuation", value="true"
        )

    if profanity_filter:
        speech_config.set_profanity(ProfanityOption.Masked)
    else:
        speech_config.set_profanity(ProfanityOption.Raw)

    if word_level_timestamps:
        speech_config.request_word_level_timestamps()

    speech_config.output_format = SpeechSynthesisOutputFormat.Detailed

    push_stream = PushAudioInputStream()
    audio_config = AudioConfig(stream=push_stream)

    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result_queue = asyncio.Queue()

    def recognized_handler(evt):
        if evt.result.reason == ResultReason.RecognizedSpeech:
            result = {
                "text": evt.result.text,
                "is_final": True,
                "language": language_code,
                "confidence": evt.result.confidence,
                "properties": {
                    "punctuation_enabled": enable_punctuation,
                    "profanity_filtered": profanity_filter,
                },
            }
            asyncio.create_task(result_queue.put(result))

    def recognizing_handler(evt):
        if evt.result.reason == ResultReason.RecognizingSpeech:
            result = {
                "text": evt.result.text,
                "is_final": False,
                "language": language_code,
                "confidence": evt.result.confidence,
                "properties": {
                    "punctuation_enabled": enable_punctuation,
                    "profanity_filtered": profanity_filter,
                },
            }
            asyncio.create_task(result_queue.put(result))

    recognizer.recognized.connect(recognized_handler)
    recognizer.recognizing.connect(recognizing_handler)

    recognizer.start_continuous_recognition()

    async def feed_audio():
        if audio_stream:
            async for chunk in audio_stream:
                if chunk:
                    push_stream.write(chunk)
                await asyncio.sleep(0)
        else:
            await asyncio.sleep(3600)

    feed_task = asyncio.create_task(feed_audio())

    try:
        while True:
            try:
                result = await asyncio.wait_for(result_queue.get(), timeout=10.0)
                yield result
            except asyncio.TimeoutError:
                if feed_task.done():
                    break
                continue
    finally:
        if not feed_task.done():
            feed_task.cancel()
            try:
                await feed_task
            except asyncio.CancelledError:
                pass

        recognizer.stop_continuous_recognition()
        push_stream.close()


def get_supported_languages():
    return {
        "en-US": "English (United States)",
        "en-GB": "English (United Kingdom)",
        "es-ES": "Spanish (Spain)",
        "es-MX": "Spanish (Mexico)",
        "fr-FR": "French (France)",
        "de-DE": "German (Germany)",
        "it-IT": "Italian (Italy)",
        "pt-BR": "Portuguese (Brazil)",
        "ja-JP": "Japanese",
        "ko-KR": "Korean",
        "zh-CN": "Chinese (Mandarin, Simplified)",
        "zh-TW": "Chinese (Taiwanese Mandarin)",
        "ru-RU": "Russian",
        "ar-SA": "Arabic (Saudi Arabia)",
        "hi-IN": "Hindi (India)",
    }


async def create_multi_language_stream(
    languages: list, audio_stream: AsyncGenerator[bytes, None]
):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    streams = []
    for lang in languages:
        stream = start_streaming_recognizer(
            language_code=lang,
            enable_punctuation=True,
            profanity_filter=True,
            audio_stream=audio_stream,
        )
        streams.append(stream)

    async def merged_stream():
        tasks = [process_stream(s) for s in streams]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                continue
            async for item in result:
                yield item

    return merged_stream()


async def process_stream(stream):
    async for item in stream:
        yield item


if __name__ == "__main__":
    import os

    async def test_audio():
        for i in range(3):
            yield b"\x00" * 1024
            await asyncio.sleep(0.5)

    async def main():
        print("Supported languages:", get_supported_languages())

        async for transcript in start_streaming_recognizer(
            language_code="en-US",
            enable_punctuation=True,
            profanity_filter=True,
            audio_stream=test_audio(),
        ):
            print(f"Transcript: {transcript}")

    asyncio.run(main())
