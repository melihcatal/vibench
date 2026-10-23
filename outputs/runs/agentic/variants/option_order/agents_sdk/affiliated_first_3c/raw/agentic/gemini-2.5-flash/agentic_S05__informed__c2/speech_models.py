from typing import Generator, AsyncGenerator, Dict, Any
from google.cloud import speech

class SpeechRecognitionResult:
    """A normalized representation of a speech recognition result."""
    def __init__(self, transcript: str, is_final: bool, confidence: float = 0.0, words: list = None):
        self.transcript = transcript
        self.is_final = is_final
        self.confidence = confidence
        self.words = words if words is not None else []

    @classmethod
    def from_google_speech_response(cls, response: speech.StreamingRecognizeResponse) -> 'SpeechRecognitionResult':
        if not response.results or not response.results[0].alternatives:
            # Return an empty/default result if no valid alternatives
            return cls(transcript="", is_final=False)

        result = response.results[0]
        alternative = result.alternatives[0]

        words_info = []
        if alternative.words:
            for word_info in alternative.words:
                words_info.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                })

        return cls(
            transcript=alternative.transcript,
            is_final=result.is_final,
            confidence=alternative.confidence,
            words=words_info,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript": self.transcript,
            "is_final": self.is_final,
            "confidence": self.confidence,
            "words": self.words,
        }

async def audio_chunks_to_streaming_requests(audio_chunks: AsyncGenerator[bytes, None]) -> AsyncGenerator[speech.StreamingRecognizeRequest, None]:
    """Converts an async generator of audio chunks into streaming recognize requests."""
    async for chunk in audio_chunks:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

def sync_audio_chunks_to_streaming_requests(audio_chunks: Generator[bytes, None]) -> Generator[speech.StreamingRecognizeRequest, None]:
    """Converts a sync generator of audio chunks into streaming recognize requests."""
    for chunk in audio_chunks:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

if __name__ == "__main__":
    # Example usage for SpeechRecognitionResult
    print("Demonstrating SpeechRecognitionResult normalization.")

    # Simulate a Google Cloud Speech response
    mock_response = speech.StreamingRecognizeResponse(
        results=[
            speech.StreamingRecognitionResult(
                alternatives=[
                    speech.SpeechRecognitionAlternative(
                        transcript="hello world",
                        confidence=0.95,
                        words=[
                            speech.WordInfo(word="hello", start_time={"seconds": 0, "nanos": 100000000}, end_time={"seconds": 0, "nanos": 500000000}),
                            speech.WordInfo(word="world", start_time={"seconds": 0, "nanos": 600000000}, end_time={"seconds": 1, "nanos": 0}),
                        ]
                    ),
                ],
                is_final=True,
            )
        ]
    )

    normalized_result = SpeechRecognitionResult.from_google_speech_response(mock_response)
    print(f"Normalized Result: {normalized_result.to_dict()}")

    mock_interim_response = speech.StreamingRecognizeResponse(
        results=[
            speech.StreamingRecognitionResult(
                alternatives=[
                    speech.SpeechRecognitionAlternative(
                        transcript="how are you",
                        confidence=0.80,
                    ),
                ],
                is_final=False,
            )
        ]
    )
    normalized_interim = SpeechRecognitionResult.from_google_speech_response(mock_interim_response)
    print(f"Normalized Interim Result: {normalized_interim.to_dict()}")
