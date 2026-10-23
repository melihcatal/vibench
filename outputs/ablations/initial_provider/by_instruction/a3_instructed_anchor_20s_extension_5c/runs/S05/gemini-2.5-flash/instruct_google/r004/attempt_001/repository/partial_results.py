def handle_partial_results(responses):
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            yield {"type": "final", "transcript": transcript, "confidence": result.alternatives[0].confidence}
        else:
            yield {"type": "partial", "transcript": transcript}
