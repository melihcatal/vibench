from google.cloud import speech_v1p1beta1 as speech

# Assuming `response_iterator` is an iterable of StreamingRecognizeResponse objects
def handle_streaming_recognition_events(response_iterator):
    for response in response_iterator:
        # Check if the response contains any results
        if not response.results:
            continue

        # The `results` list is populated incrementally, with the first result being the most stable.
        # The last result is typically the current partial or final transcript.
        for result in response.results:
            # `is_final` indicates if the transcript is stable and complete.
            # For partial results, `is_final` will be False.
            if result.is_final:
                print(f"Final Transcript: {result.alternatives[0].transcript}")
            else:
                print(f"Partial Transcript: {result.alternatives[0].transcript}")

if __name__ == '__main__':
    # This is a placeholder for demonstration. In a real scenario,
    # `response_iterator` would come from `client.streaming_recognize`.
    # We'll simulate some responses.

    # Example of a partial and then a final response
    mock_responses = [
        speech.StreamingRecognizeResponse(
            results=[
                speech.StreamingRecognitionResult(
                    alternatives=[speech.SpeechRecognitionAlternative(transcript="how are ")],
                    is_final=False
                )
            ]
        ),
        speech.StreamingRecognizeResponse(
            results=[
                speech.StreamingRecognitionResult(
                    alternatives=[speech.SpeechRecognitionAlternative(transcript="how are you ")],
                    is_final=False
                )
            ]
        ),
        speech.StreamingRecognizeResponse(
            results=[
                speech.StreamingRecognitionResult(
                    alternatives=[speech.SpeechRecognitionAlternative(transcript="how are you doing")],
                    is_final=True
                )
            ]
        ),
        speech.StreamingRecognizeResponse(
            results=[
                speech.StreamingRecognitionResult(
                    alternatives=[speech.SpeechRecognitionAlternative(transcript="good morning")],
                    is_final=False
                )
            ]
        ),
        speech.StreamingRecognizeResponse(
            results=[
                speech.StreamingRecognitionResult(
                    alternatives=[speech.SpeechRecognitionAlternative(transcript="good morning everyone")],
                    is_final=True
                )
            ]
        ),
    ]

    print("Simulating streaming recognition events...")
    handle_streaming_recognition_events(mock_responses)
