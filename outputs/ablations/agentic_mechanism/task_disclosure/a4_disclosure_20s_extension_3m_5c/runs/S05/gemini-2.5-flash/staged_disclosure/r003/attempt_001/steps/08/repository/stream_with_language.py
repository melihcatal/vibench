from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

def stream_recognize_with_language_and_punctuation(
    
) -> None:
    """Streams speech recognition with language and punctuation settings.
    For more information on setting up credentials, please refer to:
    https://cloud.google.com/docs/authentication/getting-started
    """

    client = speech.SpeechClient()

    # Configure the recognition request
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",  # Specify the language code
        enable_automatic_punctuation=True,  # Enable automatic punctuation
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # In a real application, you would stream audio from a microphone or a file
    # For demonstration, we'll use a dummy generator
    def request_generator():
        # Replace this with actual audio input
        yield types.StreamingRecognizeRequest(audio_content=b"") 

    requests = request_generator()

    responses = client.streaming_recognize(streaming_config, requests)

    print("Streaming recognition started. Press Ctrl+C to stop.")

    for response in responses:
        # Process the streaming responses
        if response.results:
            for result in response.results:
                print(f"Transcript: {result.alternatives[0].transcript}")

if __name__ == "__main__":
    stream_recognize_with_language_and_punctuation()
