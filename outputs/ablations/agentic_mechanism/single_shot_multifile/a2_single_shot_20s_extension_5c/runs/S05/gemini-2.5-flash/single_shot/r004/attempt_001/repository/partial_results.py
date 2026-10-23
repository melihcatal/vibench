from typing import Generator, Iterator
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_models import TranscriptChunk, parse_gcsst_response

def process_streaming_responses(responses_generator: Iterator[types.StreamingRecognizeResponse]) -> Generator[TranscriptChunk, None, None]:
    """Processes a generator of Google Cloud Speech-to-Text streaming responses.

    Args:
        responses_generator: An iterator yielding StreamingRecognizeResponse objects.

    Yields:
        TranscriptChunk: Processed transcript chunks, including interim and final results.
    """
    for response in responses_generator:
        if not response.results:  # No results for this response
            continue

        # The `results` list is currently only populated with one item.
        result = response.results[0]

        if not result.alternatives:  # No alternatives for this result
            continue

        # The `alternatives` list is currently only populated with one item.
        alternative = result.alternatives[0]

        transcript_chunk = parse_gcsst_response(result, alternative)
        if transcript_chunk:
            yield transcript_chunk
