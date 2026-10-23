import asyncio
from typing import AsyncIterator, Tuple

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import (
    load_config,
    build_recognizer_path,
    build_streaming_config,
    validate_config,
)
from speech_models import StreamingRecognitionResult, WordInfo


def create_audio_generator(sample_rate: int = 16000, chunk_duration_ms: int = 100):
    import sounddevice as sd
    import queue

    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time_info, status):
        audio_queue.put(indata.tobytes())

    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        callback=audio_callback,
        blocksize=int(sample_rate * chunk_duration_ms / 1000),
    )
    stream.start()

    async def yield_audio():
        loop = asyncio.get_event_loop()
        while True:
            try:
                chunk = await loop.run_in_executor(None, audio_queue.get, True, 1.0)
                yield chunk
            except Exception:
                break

    return yield_audio()


async def stream_microphone(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
) -> AsyncIterator[Tuple[StreamingRecognitionResult, bool]]:
    config = load_config()
    validate_config(config)
    config.language_code = language_code
    config.sample_rate_hertz = sample_rate_hertz

    client = speech_v2.SpeechClient()
    recognizer = build_recognizer_path(config)
    streaming_config = build_streaming_config(config)

    config_request = cloud_speech.StreamingRecognitionConfig(
        config=cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=[language_code],
            model=config.model,
            features=cloud_speech.RecognitionFeatures(
                enable_automatic_punctuation=config.enable_automatic_punctuation,
                enable_word_time_offsets=config.enable_word_time_offsets,
            ),
        ),
    )

    audio_generator = create_audio_generator(sample_rate_hertz)

    def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(streaming_config=config_request)
        for chunk in audio_generator:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(
        recognizer=recognizer,
        requests=request_generator(),
    )

    for response in responses:
        for result in response.results:
            words = [
                WordInfo(
                    word=w.word,
                    start_offset_seconds=w.start_offset.seconds
                    + w.start_offset.microseconds / 1_000_000,
                    end_offset_seconds=w.end_offset.seconds
                    + w.end_offset.microseconds / 1_000_000,
                    confidence=w.confidence,
                )
                for w in result.word_info
            ]
            recognition_result = StreamingRecognitionResult(
                transcript=result.alternatives[0].transcript,
                is_final=result.is_final,
                stability=result.stability,
                confidence=result.alternatives[0].confidence,
                words=words,
                language_code=language_code,
            )
            yield recognition_result, result.is_final
