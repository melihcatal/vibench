from google.cloud.speech_v1p1beta1 import types

def process_streaming_responses(responses):
    for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            first_alternative = result.alternatives[0]
            transcript_info = {
                "transcript": first_alternative.transcript,
                "is_final": result.is_final,
                "confidence": first_alternative.confidence,
            }
            yield transcript_info