from google.cloud import speech


def normalize_response(response):
    results = []
    for result in response.results:
        if result.alternatives:
            results.append({
                "text": result.alternatives[0].transcript,
                "is_final": result.is_final
            })
    return results