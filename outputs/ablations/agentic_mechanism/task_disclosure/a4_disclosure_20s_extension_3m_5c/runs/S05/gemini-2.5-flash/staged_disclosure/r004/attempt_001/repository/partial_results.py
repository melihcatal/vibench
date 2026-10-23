
import os
from google.cloud import speech

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives. We print the first alternative of the first
    result only. We also print whether a transcript is finished or not.
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
            print(transcript + overwrite_chars, end='\r')
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)
            num_chars_printed = 0

def streaming_recognize(audio_file_path):
    """Streams audio from a file to Google Cloud Speech-to-Text API."""

    # Set up Google Cloud credentials (e.g., via environment variable GOOGLE_APPLICATION_CREDENTIALS)
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set to the path of your service account key.

    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream audio in smaller chunks
    def generate_requests():
        yield speech.StreamingRecognizeRequest(audio_content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    requests = generate_requests()
    responses = client.streaming_recognize(streaming_config, requests)

    listen_print_loop(responses)

if __name__ == "__main__":
    # This is a placeholder for an actual audio file.
    # Replace 'path/to/your/audio.raw' with the actual path to a .raw audio file.
    # The audio file should be 16-bit, 16000 Hz, mono, LINEAR16 encoded.
    # For example: streaming_recognize("resources/audio.raw")
    print("Please provide an audio file path to the 'streaming_recognize' function.")
    print("Example: streaming_recognize('path/to/your/audio.raw')")
