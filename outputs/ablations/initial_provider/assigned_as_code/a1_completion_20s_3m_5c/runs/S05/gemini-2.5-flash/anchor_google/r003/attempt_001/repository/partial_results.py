from speech_models import StreamingRecognitionResult

def handle_partial_results(recognition_result: StreamingRecognitionResult):
    """Handles partial streaming recognition results."""
    if not recognition_result.is_final:
        print(f"Partial Transcript: {recognition_result.transcript}")

def handle_final_results(recognition_result: StreamingRecognitionResult):
    """Handles final streaming recognition results."""
    if recognition_result.is_final:
        print(f"Final Transcript: {recognition_result.transcript}")
        # Here you might trigger other downstream processes like translation, safety check, summary
        return recognition_result.transcript
    return None

def process_streaming_transcription(results_generator):
    """Processes a generator of StreamingRecognitionResult objects."""
    for result in results_generator:
        handle_partial_results(result)
        final_transcript = handle_final_results(result)
        if final_transcript:
            yield final_transcript
