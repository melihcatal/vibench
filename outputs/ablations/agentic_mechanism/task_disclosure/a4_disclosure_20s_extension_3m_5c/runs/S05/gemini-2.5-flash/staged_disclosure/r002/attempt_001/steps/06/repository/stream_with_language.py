import google.cloud.speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import io

def stream_with_language_punctuation():
    client = speech.SpeechClient()

    config = speech.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # In a real application, audio input would come from a microphone.
    # For demonstration, we'll use a placeholder for the audio content.
    # Replace this with actual audio input.
    def request_generator():
        # Simulate a small audio chunk. In a real scenario, this would be
        # a continuous stream of audio bytes from a microphone.
        yield speech.types.StreamingRecognizeRequest(audio_content=b"") 

    requests = request_generator()

    responses = client.streaming_recognize(streaming_config, requests)

    print("Listening for speech (with language and punctuation enabled)...")

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        print(f"Transcript: {transcript}")

if __name__ == "__main__":
    stream_with_language_punctuation()
