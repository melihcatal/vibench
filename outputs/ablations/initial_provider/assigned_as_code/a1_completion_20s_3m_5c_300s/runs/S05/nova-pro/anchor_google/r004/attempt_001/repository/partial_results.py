from google.cloud import speech


def partial_results(response):
    for result in response.results:
        if result.alternatives:
            yield {"text": result.alternatives[0].transcript, "is_final": result.is_final}