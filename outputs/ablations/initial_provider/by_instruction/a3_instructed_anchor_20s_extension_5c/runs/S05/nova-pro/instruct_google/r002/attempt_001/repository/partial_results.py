from speech_client import speech_client

# Handle partial and final streaming recognition events
def partial_results(responses):
    for response in responses:
        for result in response.results:
            if not result.is_final:
                print(f"Interim transcript: {result.alternatives[0].transcript}")
            else:
                print(f"Final transcript: {result.alternatives[0].transcript}")