import asyncio
from typing import AsyncIterator, Callable, Dict, List, Optional, Tuple

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import load_config, build_recognizer_path, validate_config
from speech_models import (
    StreamingRecognitionResult,
    WordInfo,
    normalize_transcript,
    merge_results,
)


class PartialResultHandler:
    def __init__(
        self,
        on_partial: Optional[Callable[[StreamingRecognitionResult], None]] = None,
        on_final: Optional[Callable[[StreamingRecognitionResult], None]] = None,
        on_transcript_update: Optional[Callable[[str, bool], None]] = None,
    ):
        self.on_partial = on_partial
        self.on_final = on_final
        self.on_transcript_update = on_transcript_update
        self._partial_results: List[StreamingRecognitionResult] = []
        self._final_results: List[StreamingRecognitionResult] = []
        self._current_partial: Optional[StreamingRecognitionResult] = None

    def handle_result(self, result: StreamingRecognitionResult) -> None:
        if result.is_final:
            self._final_results.append(result)
            self._partial_results = []
            self._current_partial = None
            if self.on_final:
                self.on_final(result)
        else:
            self._current_partial = result
            if self.on_partial:
                self.on_partial(result)

        if self.on_transcript_update:
            combined = merge_results(self._final_results + self._partial_results)
            self.on_transcript_update(combined, result.is_final)

    def get_full_transcript(self) -> str:
        return merge_results(self._final_results + self._partial_results)

    def get_final_transcript(self) -> str:
        return merge_results(self._final_results)

    def get_stability(self) -> float:
        if self._current_partial:
            return self._current_partial.stability
        return 1.0


async def process_streaming_results(
    responses: AsyncIterator[cloud_speech.StreamingRecognizeResponse],
    handler: PartialResultHandler,
    language_code: str = "en-US",
) -> AsyncIterator[Tuple[StreamingRecognitionResult, bool]]:
    async for response in responses:
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
            handler.handle_result(recognition_result)
            yield recognition_result, result.is_final


async def stream_with_partial_handling(
    audio_source: AsyncIterator[bytes],
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    on_partial: Optional[Callable[[StreamingRecognitionResult], None]] = None,
    on_final: Optional[Callable[[StreamingRecognitionResult], None]] = None,
) -> AsyncIterator[str]:
    config = load_config()
    validate_config(config)
    config.language_code = language_code

    client = speech_v2.SpeechClient()
    recognizer = build_recognizer_path(config)

    handler = PartialResultHandler(on_partial=on_partial, on_final=on_final)

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=[language_code],
            model=config.model,
            features=cloud_speech.RecognitionFeatures(
                enable_automatic_punctuation=enable_punctuation,
                enable_word_time_offsets=config.enable_word_time_offsets,
            ),
        ),
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_source:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)
        yield cloud_speech.StreamingRecognizeRequest(audio=b"")

    responses = client.streaming_recognize(
        recognizer=recognizer,
        requests=request_generator(),
    )

    async for result, is_final in process_streaming_results(
        responses, handler, language_code
    ):
        yield handler.get_full_transcript()
