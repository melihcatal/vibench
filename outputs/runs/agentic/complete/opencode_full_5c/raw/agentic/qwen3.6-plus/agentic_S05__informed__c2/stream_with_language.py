import asyncio
from typing import AsyncGenerator, Dict, List, Optional

from speech_client import (
    create_deepgram_client,
    build_live_options,
    register_default_handlers,
)
from speech_models import TranscriptResult, parse_deepgram_result
from partial_results import PartialResultHandler, create_deepgram_callback_handler
from deepgram.clients.live.v1 import LiveTranscriptionEvents

SUPPORTED_LANGUAGES = {
    "en-US": "English (US)",
    "en-GB": "English (UK)",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "pt-BR": "Portuguese (Brazil)",
    "zh": "Chinese",
    "zh-CN": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "nl": "Dutch",
    "pl": "Polish",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "no": "Norwegian",
}


class StreamingRecognizer:
    def __init__(
        self,
        model: str = "nova-2",
        language: str = "en-US",
        sample_rate: int = 16000,
        channels: int = 1,
        punctuate: bool = True,
        smart_format: bool = True,
        interim_results: bool = True,
        profanity_filter: bool = False,
        diarize: bool = False,
        redact: Optional[List[str]] = None,
        keywords: Optional[List[tuple]] = None,
        custom_topics: Optional[List[str]] = None,
        vad_events: bool = True,
    ):
        self.model = model
        self.language = language
        self.sample_rate = sample_rate
        self.channels = channels
        self.punctuate = punctuate
        self.smart_format = smart_format
        self.interim_results = interim_results
        self.profanity_filter = profanity_filter
        self.diarize = diarize
        self.redact = redact or []
        self.keywords = keywords or []
        self.custom_topics = custom_topics or []
        self.vad_events = vad_events
        self._client = None
        self._ws = None
        self._handler = None

    def validate_language(self) -> bool:
        return self.language in SUPPORTED_LANGUAGES

    def build_options(self):
        extra = {}
        if self.redact:
            extra["redact"] = self.redact
        if self.keywords:
            extra["keywords"] = self.keywords
        if self.custom_topics:
            extra["custom_topics"] = self.custom_topics

        return build_live_options(
            model=self.model,
            language=self.language,
            sample_rate=self.sample_rate,
            channels=self.channels,
            punctuate=self.punctuate,
            smart_format=self.smart_format,
            interim_results=self.interim_results,
            profanity_filter=self.profanity_filter,
            diarize=self.diarize,
            vad_events=self.vad_events,
            extra=extra if extra else None,
        )

    async def start(
        self,
        on_interim=None,
        on_final=None,
        on_error=None,
    ):
        self._client = create_deepgram_client()
        options = self.build_options()

        self._handler = PartialResultHandler(
            on_interim=on_interim,
            on_final=on_final,
            on_error=on_error,
        )

        transcript_callback = create_deepgram_callback_handler(self._handler)

        self._ws = await self._client.listen.asyncwebsocket.v("1").start(options)
        self._ws.on(LiveTranscriptionEvents.Transcript, transcript_callback)

        return self._ws

    async def send_audio(self, audio_data: bytes):
        if self._ws:
            await self._ws.send(audio_data)

    async def finalize(self):
        if self._ws:
            await self._ws.finalize()

    async def close(self):
        if self._ws:
            await self._ws.finish()

    def get_final_transcript(self) -> str:
        if self._handler:
            return self._handler.get_final_transcript()
        return ""

    def get_results(self):
        if self._handler:
            return self._handler.get_all_results()
        return [], []


async def create_streaming_recognizer_with_language(
    language: str = "en-US",
    model: str = "nova-2",
    sample_rate: int = 16000,
    channels: int = 1,
    punctuate: bool = True,
    smart_format: bool = True,
    interim_results: bool = True,
    profanity_filter: bool = False,
    diarize: bool = False,
    redact: Optional[List[str]] = None,
    keywords: Optional[List[tuple]] = None,
) -> StreamingRecognizer:
    recognizer = StreamingRecognizer(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=channels,
        punctuate=punctuate,
        smart_format=smart_format,
        interim_results=interim_results,
        profanity_filter=profanity_filter,
        diarize=diarize,
        redact=redact,
        keywords=keywords,
    )

    if not recognizer.validate_language():
        raise ValueError(
            f"Unsupported language: {language}. "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
        )

    return recognizer


async def stream_with_language_settings(
    audio_source: AsyncGenerator[bytes, None],
    language: str = "en-US",
    model: str = "nova-2",
    sample_rate: int = 16000,
    channels: int = 1,
    punctuate: bool = True,
    smart_format: bool = True,
    interim_results: bool = True,
    profanity_filter: bool = False,
    diarize: bool = False,
) -> AsyncGenerator[TranscriptResult, None]:
    recognizer = await create_streaming_recognizer_with_language(
        language=language,
        model=model,
        sample_rate=sample_rate,
        channels=channels,
        punctuate=punctuate,
        smart_format=smart_format,
        interim_results=interim_results,
        profanity_filter=profanity_filter,
        diarize=diarize,
    )

    result_queue: asyncio.Queue = asyncio.Queue()
    stop_event = asyncio.Event()

    def on_interim(result: TranscriptResult):
        result_queue.put_nowait(result)

    def on_final(result: TranscriptResult):
        result_queue.put_nowait(result)

    ws = await recognizer.start(
        on_interim=on_interim,
        on_final=on_final,
    )

    async def send_audio():
        async for audio_data in audio_source:
            await recognizer.send_audio(audio_data)
        await recognizer.finalize()
        stop_event.set()

    send_task = asyncio.create_task(send_audio())

    try:
        while not stop_event.is_set():
            try:
                result = await asyncio.wait_for(result_queue.get(), timeout=1.0)
                yield result
            except asyncio.TimeoutError:
                continue
    finally:
        send_task.cancel()
        await recognizer.close()
