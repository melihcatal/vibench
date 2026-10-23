from google.cloud import speech

def handle_recognition_events(responses):
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            print(f"Final: {transcript}")
            yield transcript, True
        else:
            print(f"Partial: {transcript}")
            yield transcript, False
