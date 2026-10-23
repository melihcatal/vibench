import asyncio
from typing import Optional, AsyncGenerator

from deepgram import DeepgramClient, LiveOptions

from speech_client import create_deepgram_client, build_live_options
from speech_models import (
    StreamRequest,
    parse_deepgram_response,
    StreamingTranscriptResponse,
    NormalizedTranscript,
)


async def start_streaming_recognizer(
    audio_source: AsyncGenerator[bytes, None],
    api_key: Optional[str] = None,
    language: str = "en",
    model: str = "nova-2",
    punctuate: bool = True,
    interim_results: bool = True,
    smart_format: bool = True,
    profanity_filter: bool = False,
    diarize: bool = False,
    keywords: Optional[list] = None,
    sample_rate: int = 16000,
    channels: int = 1,
    encoding: str = "linear16",
) -> AsyncGenerator[NormalizedTranscript, None]:
    client = create_deepgram_client(api_key)

    options = LiveOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
        smart_format=smart_format,
        profanity_filter=profanity_filter,
        diarize=diarize,
        keywords=keywords or [],
        encoding=encoding,
        sample_rate=sample_rate,
        channels=channels,
    )

    result_queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def on_transcript(self, result, **kwargs):
        raw = result.to_dict()
        parsed = parse_deepgram_response(raw)
        is_final = raw.get("is_final", False)
        for alt in parsed.alternatives:
            norm = NormalizedTranscript(
                text=alt.transcript,
                confidence=alt.confidence,
                start_time=parsed.start,
                end_time=parsed.start + parsed.duration,
                is_final=is_final,
                words=alt.words,
                language=language,
            )
            asyncio.run_coroutine_threadsafe(result_queue.put(norm), loop)

    def on_error(self, error, **kwargs):
        pass

    dg_connection = client.listen.live.v("1")
    dg_connection.on("transcript", on_transcript)
    dg_connection.on("error", on_error)

    await asyncio.to_thread(dg_connection.start, options)

    async def send_audio():
        async for chunk in audio_source:
            await asyncio.to_thread(dg_connection.send, chunk)

    send_task = asyncio.create_task(send_audio())

    try:
        while True:
            transcript = await result_queue.get()
            yield transcript
    finally:
        send_task.cancel()
        await asyncio.to_thread(dg_connection.finish)


async def start_streaming_with_request(
    audio_source: AsyncGenerator[bytes, None],
    request: StreamRequest,
    api_key: Optional[str] = None,
) -> AsyncGenerator[NormalizedTranscript, None]:
    async for transcript in start_streaming_recognizer(
        audio_source=audio_source,
        api_key=api_key,
        language=request.language,
        model=request.model,
        punctuate=request.punctuate,
        interim_results=request.interim_results,
        smart_format=request.smart_format,
        profanity_filter=request.profanity_filter,
        diarize=request.diarize,
        keywords=request.keywords,
        sample_rate=request.sample_rate,
        channels=request.channels,
        encoding=request.encoding,
    ):
        yield transcript
