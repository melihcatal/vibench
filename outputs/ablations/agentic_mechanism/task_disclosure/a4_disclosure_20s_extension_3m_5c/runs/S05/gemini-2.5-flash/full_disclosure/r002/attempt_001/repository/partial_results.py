from google.cloud import speech_v1p1beta1 as speech

def handle_recognition_event(response):
    """
    Handles streaming recognition events, distinguishing between partial and final results.

    Args:
        response: The StreamingRecognizeResponse object from Google Cloud Speech-to-Text.
    """
    for result in response.results:
        if result.is_final:
            print(f"Final transcript: {result.alternatives[0].transcript}")
        else:
            print(f"Partial transcript: {result.alternatives[0].transcript}")

if __name__ == '__main__':
    # This is an example of how the function might be used.
    # In a real application, 'response' would come from a live streaming recognition session.
    
    # Example for a partial result
    mock_partial_response = speech.StreamingRecognizeResponse(
        results=[
            speech.StreamingRecognitionResult(
                alternatives=[speech.SpeechRecognitionAlternative(transcript="hello wor")],
                is_final=False
            )
        ]
    )
    print("--- Simulating Partial Result ---")
    handle_recognition_event(mock_partial_response)

    # Example for a final result
    mock_final_response = speech.StreamingRecognizeResponse(
        results=[
            speech.StreamingRecognitionResult(
                alternatives=[speech.SpeechRecognitionAlternative(transcript="hello world.")],
                is_final=True
            )
        ]
    )
    print("
--- Simulating Final Result ---")
    handle_recognition_event(mock_final_response)
