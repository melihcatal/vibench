import google.cloud.speech_v1p1beta1 as speech

def handle_streaming_responses(responses):
    """
    Handles partial and final streaming recognition events from Google Cloud Speech-to-Text.
    """
    for response in responses:
        if not response.results:
            continue

        # The `results` list is initialized for a single result for simplicity.
        # In more complex scenarios, you might have multiple results in a single response.
        result = response.results[0]
        if not result.alternatives:
            continue

        # The `alternatives` list is initialized for a single alternative for simplicity.
        # In more complex scenarios, you might have multiple alternatives.
        transcript = result.alternatives[0].transcript

        if result.is_final:
            print(f"Final transcript: {transcript}")
        else:
            print(f"Partial transcript: {transcript}")
