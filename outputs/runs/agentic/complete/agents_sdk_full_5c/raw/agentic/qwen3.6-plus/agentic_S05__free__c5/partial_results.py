"""Handle partial and final streaming recognition events from Google Cloud Speech-to-Text.

Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
SDK: google-cloud-speech (google.cloud.speech_v1p1beta1)
"""

from typing import Callable, Generator, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_speech_client, build_streaming_config
from speech_models import (
    StreamingResponseBatch,
    StreamingTranscriptResult,
    filter_final_results,
    filter_interim_results,
    normalize_transcript_text,
)


class StreamingResultHandler:
    """Handler for partial (interim) and final streaming recognition events.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
    """

    def __init__(
        self,
        on_interim: Optional[Callable[[StreamingTranscriptResult], None]] = None,
        on_final: Optional[Callable[[StreamingTranscriptResult], None]] = None,
        on_batch: Optional[Callable[[StreamingResponseBatch], None]] = None,
    ):
        self.on_interim = on_interim
        self.on_final = on_final
        self.on_batch = on_batch
        self._final_transcripts: list[StreamingTranscriptResult] = []
        self._interim_transcripts: list[StreamingTranscriptResult] = []

    def handle_response(self, response: speech.StreamingRecognizeResponse) -> None:
        """Process a Google Cloud StreamingRecognizeResponse.

        Separates interim and final results, normalizes them, and triggers callbacks.

        Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
        """
        batch = StreamingResponseBatch.from_google_response(response)

        if self.on_batch:
            self.on_batch(batch)

        for result in batch.results:
            result.transcript = normalize_transcript_text(result.transcript)

            if result.is_final:
                self._final_transcripts.append(result)
                if self.on_final:
                    self.on_final(result)
            else:
                self._interim_transcripts.append(result)
                if self.on_interim:
                    self.on_interim(result)

    @property
    def final_transcripts(self) -> list[StreamingTranscriptResult]:
        """Return all final transcript results."""
        return list(self._final_transcripts)

    @property
    def interim_transcripts(self) -> list[StreamingTranscriptResult]:
        """Return all interim transcript results."""
        return list(self._interim_transcripts)

    @property
    def full_transcript(self) -> str:
        """Concatenate all final transcripts into a single string."""
        return " ".join(r.transcript for r in self._final_transcripts if r.transcript)


def process_streaming_results(
    audio_source: Generator[bytes, None, None],
    language_code: str = "en-US",
    on_interim: Optional[Callable[[StreamingTranscriptResult], None]] = None,
    on_final: Optional[Callable[[StreamingTranscriptResult], None]] = None,
) -> StreamingResultHandler:
    """Process streaming audio results with interim and final callbacks.

    Uses google-cloud-speech SDK to connect to speech.googleapis.com.

    Args:
        audio_source: Generator yielding audio bytes (LINEAR16 PCM)
        language_code: BCP-47 language code
        on_interim: Callback for interim (partial) results
        on_final: Callback for final results

    Returns:
        StreamingResultHandler with all processed results
    """
    client = create_speech_client()
    streaming_config = build_streaming_config(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="default",
        enable_interim_results=True,
    )

    handler = StreamingResultHandler(on_interim=on_interim, on_final=on_final)

    def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        for chunk in audio_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        if response.results:
            handler.handle_response(response)

    return handler


def extract_partial_text(
    response: speech.StreamingRecognizeResponse,
) -> tuple[str, str]:
    """Extract partial (interim) and final text from a Google Cloud response.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)

    Returns:
        Tuple of (interim_text, final_text)
    """
    interim_parts = []
    final_parts = []

    for result in response.results:
        if result.alternatives:
            text = result.alternatives[0].transcript
            if result.is_final:
                final_parts.append(normalize_transcript_text(text))
            else:
                interim_parts.append(normalize_transcript_text(text))

    return (" ".join(interim_parts), " ".join(final_parts))
