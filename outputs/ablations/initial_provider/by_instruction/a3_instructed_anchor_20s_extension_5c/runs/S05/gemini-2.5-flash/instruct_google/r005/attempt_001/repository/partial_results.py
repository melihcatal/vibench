def handle_recognition_events(responses):
    """Handles streaming recognition responses, yielding interim and final transcripts.

    Args:
        responses: An iterable of Google Cloud Speech-to-Text StreamingRecognizeResponse objects.

    Yields:
        Tuples of (transcript: str, is_final: bool).
    """
    for response in responses:
        if not response.results:
            continue

        # The `results` list is populated in reverse order for streaming recognition.
        # The first result in the list is the most recent one.
        result = response.results[0]

        if not result.alternatives:
            continue

        # The `alternatives` list is populated in order of transcription accuracy.
        # The first alternative is the most probable one.
        transcript = result.alternatives[0].transcript
        is_final = result.is_final

        yield transcript, is_final
