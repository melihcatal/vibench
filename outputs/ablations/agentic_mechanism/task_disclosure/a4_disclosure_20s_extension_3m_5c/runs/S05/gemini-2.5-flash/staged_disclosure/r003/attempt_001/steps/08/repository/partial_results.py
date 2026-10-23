import os
import io

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech

# Import the AudioSegment library for processing audio files
from pydub import AudioSegment

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# Replace 'path/to/your/credentials.json' with the actual path to your service account key file
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response is provided
    by the API. Each response may contain multiple results, and each result may contain
    multiple alternatives that correspond to a portion of the spoken utterance.
    Each alternative contains detected words and certain attributes useful for
    plotting an animation of speech through time. We print the best alternative for
    the audio.
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

def stream_recognize(audio_file_path):
    """Streams audio from a file to the Google Cloud Speech-to-Text API and
    prints partial and final recognition results."""

    # Load audio file using pydub
    audio = AudioSegment.from_file(audio_file_path)
    
    # Resample to 16kHz if necessary for the API
    if audio.frame_rate != 16000:
        audio = audio.set_frame_rate(16000)

    # Convert audio to raw 16-bit PCM (mono)
    audio = audio.set_channels(1)
    audio = audio.set_sample_width(2)
    
    content = audio.raw_data

    client = speech.SpeechClient()

    # The `encoding` and `sample_rate_hertz` must match the audio file's encoding and
    # sample rate.
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    # In practice, stream audio from a microphone or other source
    # For this example, we use a file.
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in _generate_audio_chunks(content, chunk_size=32000) # Adjust chunk_size as needed
    )

    responses = client.streaming_recognize(streaming_config, requests)

    # Now, put the transcription responses to use.
    listen_print_loop(responses)

def _generate_audio_chunks(audio_content, chunk_size):
    for i in range(0, len(audio_content), chunk_size):
        yield audio_content[i : i + chunk_size]

if __name__ == "__main__":
    # Example usage: Replace 'path/to/your/audio.wav' with an actual audio file
    # For a real application, you would typically stream from a microphone.
    print("This script demonstrates streaming recognition with Google Cloud Speech-to-Text.")
    print("Please ensure you have authenticated with Google Cloud (e.g., via GOOGLE_APPLICATION_CREDENTIALS).")
    print("To run this example, you would typically provide a path to an audio file:")
    print("  stream_recognize('path/to/your/audio.wav')")
    print("\nNote: The 'pydub' library requires 'ffmpeg' or 'libav' to be installed.")
    print("       You can install pydub using: pip install pydub")
    print("       You can install ffmpeg using: brew install ffmpeg (macOS) or apt-get install ffmpeg (Debian/Ubuntu)")
