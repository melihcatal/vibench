def handle_partial_results(stream_responses):
    for response in stream_responses:
        for result in response.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": result.is_final, "stability": result.stability}
