from speech_models import SpeechRecognitionResult

# This file processes results from Google Cloud Speech-to-Text.


def handle_recognition_event(result: SpeechRecognitionResult):
    """
    Handles a single speech recognition event, printing partial or final transcripts.

    Args:
        result: A SpeechRecognitionResult object containing the transcript and its status.
    """
    if result.is_final:
        print(f"[FINAL]: {result.transcript} (Confidence: {result.confidence:.2f})")
    else:
        print(f"[PARTIAL]: {result.transcript}")


async def process_recognition_stream(recognition_results_generator):
    """
    Asynchronously processes a stream of speech recognition results.

    Args:
        recognition_results_generator: An async generator yielding SpeechRecognitionResult objects.
    """
    async for result in recognition_results_generator:
        handle_recognition_event(result)
