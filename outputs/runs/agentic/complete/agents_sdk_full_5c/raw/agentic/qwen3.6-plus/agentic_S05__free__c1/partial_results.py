"""Handle partial and final streaming recognition events from Google Cloud Speech-to-Text."""

from typing import Iterator, Tuple

from google.cloud.speech_v1p1beta1 import types as speech_types


def handle_recognition_event(result: speech_types.StreamingRecognitionResult) -> Iterator[Tuple[str, bool, float]]:
    """Process a single StreamingRecognitionResult and yield transcript tuples.

    Extracts transcript text, finality flag, and confidence score from a Google
    Cloud Speech-to-Text streaming recognition result. Handles both interim
    (partial) and final results.

    Args:
        result: A StreamingRecognitionResult from Google Cloud Speech streaming API.

    Yields:
        Tuples of (transcript_text, is_final, confidence) for each alternative.
    """
    is_final = result.is_final
    stability = result.stability if hasattr(result, 'stability') else 0.0

    for alternative in result.alternatives:
        transcript = alternative.transcript
        confidence = alternative.confidence

        if transcript.strip():
            yield transcript, is_final, confidence


def accumulate_final_transcripts(events: Iterator[Tuple[str, bool, float]]) -> str:
    """Accumulate only final transcripts from a stream of recognition events.

    Args:
        events: Iterator of (transcript, is_final, confidence) tuples.

    Returns:
        Concatenated string of all final transcripts, separated by spaces.
    """
    final_parts = []
    for transcript, is_final, _confidence in events:
        if is_final:
            final_parts.append(transcript.strip())
    return " ".join(final_parts)


def get_best_transcript(results) -> Tuple[str, float]:
    """Extract the best transcript from a list of StreamingRecognitionResults.

    Selects the top alternative from the first final result, falling back to
    the first interim result if no final results exist.

    Args:
        results: List of StreamingRecognitionResult objects.

    Returns:
        Tuple of (best_transcript, confidence) or ("", 0.0) if none found.
    """
    final_results = [r for r in results if r.is_final and r.alternatives]
    candidates = final_results if final_results else [r for r in results if r.alternatives]

    if not candidates:
        return "", 0.0

    best = candidates[0].alternatives[0]
    return best.transcript, best.confidence
