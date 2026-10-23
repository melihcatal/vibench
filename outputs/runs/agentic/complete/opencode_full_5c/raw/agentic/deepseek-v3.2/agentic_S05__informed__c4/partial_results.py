import asyncio
from typing import AsyncGenerator, Dict, Any, List
from dataclasses import dataclass
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


@dataclass
class RecognitionEvent:
    transcript: str
    is_final: bool
    confidence: float
    language_code: str
    alternatives: List[Dict[str, Any]]
    stability: float = 0.0


class PartialResultsHandler:
    def __init__(self, language_code: str = "en-US"):
        self.client = get_speech_client()
        self.language_code = language_code
        self._partial_buffer = []
        self._final_results = []

    async def process_stream(
        self, audio_generator: AsyncGenerator[bytes, None]
    ) -> AsyncGenerator[RecognitionEvent, None]:
        config = StreamingRecognitionConfig(
            encoding="LINEAR16",
            sample_rate_hertz=16000,
            language_code=self.language_code,
            enable_automatic_punctuation=True,
            interim_results=True,
            enable_word_time_offsets=True,
        )

        responses = self.client.streaming_recognize(config, audio_generator)

        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                event = self._create_recognition_event(result)
                yield event

                if event.is_final:
                    self._final_results.append(event)
                    self._partial_buffer = []
                else:
                    self._partial_buffer.append(event)

    def _create_recognition_event(self, result) -> RecognitionEvent:
        alternatives = []
        if result.alternatives:
            for alt in result.alternatives:
                alternatives.append(
                    {
                        "transcript": alt.transcript,
                        "confidence": alt.confidence,
                        "words": [
                            {
                                "word": w.word,
                                "start_time": w.start_time,
                                "end_time": w.end_time,
                            }
                            for w in alt.words
                        ]
                        if hasattr(alt, "words")
                        else [],
                    }
                )

        main_transcript = alternatives[0]["transcript"] if alternatives else ""
        main_confidence = alternatives[0]["confidence"] if alternatives else 0.0

        return RecognitionEvent(
            transcript=main_transcript,
            is_final=result.is_final,
            confidence=main_confidence,
            language_code=self.language_code,
            alternatives=alternatives,
            stability=getattr(result, "stability", 0.0),
        )

    def get_partial_transcript(self) -> str:
        return " ".join([event.transcript for event in self._partial_buffer])

    def get_final_transcripts(self) -> List[str]:
        return [event.transcript for event in self._final_results]

    def clear_buffer(self):
        self._partial_buffer = []


async def handle_partial_results_example():
    handler = PartialResultsHandler(language_code="en-US")

    async def mock_audio():
        for i in range(10):
            yield b"\x00" * 3200
            await asyncio.sleep(0.1)

    async for event in handler.process_stream(mock_audio()):
        if event.is_final:
            print(
                f"Final result: {event.transcript} (confidence: {event.confidence:.2f})"
            )
        else:
            print(f"Partial: {event.transcript}")
            print(f"Current buffer: {handler.get_partial_transcript()}")


if __name__ == "__main__":
    asyncio.run(handle_partial_results_example())
