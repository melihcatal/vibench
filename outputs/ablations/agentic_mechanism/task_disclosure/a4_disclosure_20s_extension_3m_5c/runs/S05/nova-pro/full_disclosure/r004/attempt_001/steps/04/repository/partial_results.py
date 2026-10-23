from google.cloud import speech

def handle_streaming_recognition(response):
    for result in response.results:
        if not result.is_final:
            print(f"Partial result: {result.alternatives[0].transcript}")
        else:
            print(f"Final result: {result.alternatives[0].transcript}")

    # Additional handling logic can be added here