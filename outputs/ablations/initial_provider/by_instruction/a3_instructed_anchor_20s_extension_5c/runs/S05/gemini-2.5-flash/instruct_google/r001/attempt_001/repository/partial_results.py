from typing import Callable

from speech_models import StreamingRecognitionResponse

def handle_partial_and_final_results(
    responses: StreamingRecognitionResponse,
    partial_callback: Callable[[str], None],
    final_callback: Callable[[str], None]
):
    """Handles partial and final streaming recognition events."""

    for response in responses:
        if not response.results: 
            continue

        result = response.results[0]
        if not result.alternatives: 
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            final_callback(transcript)
        else:
            partial_callback(transcript)
