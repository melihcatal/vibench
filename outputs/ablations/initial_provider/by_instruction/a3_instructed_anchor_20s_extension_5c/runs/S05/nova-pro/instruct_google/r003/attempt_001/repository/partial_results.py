import speech_client

def partial_results(response):
    for result in response.results:
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        is_final = result.is_final
        yield transcript, is_final