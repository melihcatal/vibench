from google.cloud import speech

def handle_partial_and_final_results(responses):
    """Handles partial and final streaming recognition events."""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            print(f"Final: {transcript}")
            return transcript
        else:
            print(f"Partial: {transcript}")
            # Optionally yield partial results for real-time display
            # yield transcript
