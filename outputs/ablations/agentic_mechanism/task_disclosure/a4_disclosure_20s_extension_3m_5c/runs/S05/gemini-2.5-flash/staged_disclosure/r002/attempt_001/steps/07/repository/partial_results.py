from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response is provided
    by the API. Each response represents a portion of a streaming speech recognition
    result rather than an utterance.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            print(transcript + overwrite_chars + '\r', end='')
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)
            num_chars_printed = 0

def stream_recognize(audio_data_generator):
    """Streams audio data to Google Cloud Speech-to-Text API and processes responses."""
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_data_generator)
    responses = client.streaming_recognize(streaming_config, requests)

    listen_print_loop(responses)

if __name__ == "__main__":
    # This is a placeholder for actual audio input.
    # In a real application, `audio_data_generator` would yield chunks of audio.
    # For demonstration, we will create a dummy generator.
    def dummy_audio_generator():
        # Yield some dummy audio data (e.g., from a file or microphone)
        # In a real scenario, this would be actual byte data.
        yield b"dummy audio chunk 1"
        yield b"dummy audio chunk 2"
        # Simulate some delay or more chunks as needed
    
    # To run this example, you would typically integrate with an audio input source
    # For example, using PyAudio to capture microphone input.
    print("This script demonstrates streaming recognition using Google Cloud Speech-to-Text.")
    print("To run a full example, replace `dummy_audio_generator` with actual audio input.")
    print("You will also need to authenticate with Google Cloud, e.g., by setting GOOGLE_APPLICATION_CREDENTIALS.")
    
    # stream_recognize(dummy_audio_generator()) # Uncomment to test with dummy data
