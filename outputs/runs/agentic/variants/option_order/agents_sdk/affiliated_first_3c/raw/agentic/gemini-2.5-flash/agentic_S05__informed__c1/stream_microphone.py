import os
import io
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.oauth2 import service_account

# This is a placeholder for actual microphone input.
# In a real application, you would read audio from a microphone.
def _get_microphone_audio_generator():
    """Simulates a microphone audio stream."""
    # For demonstration, we'll yield empty bytes.
    # Replace this with actual audio input from a microphone.
    yield b''
    # Example for reading from a dummy audio file if needed for local testing:
    # with open("path/to/your/audio.raw", "rb") as audio_file:
    #     while True:
    #         chunk = audio_file.read(4096)
    #         if not chunk:
    #             break
    #         yield chunk

def stream_microphone_audio():
    """Streams microphone audio to Google Speech-to-Text and yields interim transcripts."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or a service account key is provided
    # client = speech.SpeechClient() # Uses GOOGLE_APPLICATION_CREDENTIALS by default

    # Explicitly using a service account file if needed
    # credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # credentials = service_account.Credentials.from_service_account_file(credentials_path)
    # client = speech.SpeechClient(credentials=credentials)
    
    client = speech.SpeechClient() # Using default credentials (GOOGLE_APPLICATION_CREDENTIALS)

    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in _get_microphone_audio_generator())

    print("Starting microphone streaming recognition...")
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            if result.is_final:
                print(f"Final: {result.alternatives[0].transcript}")
            else:
                print(f"Interim: {result.alternatives[0].transcript}")
            yield result.alternatives[0].transcript

if __name__ == "__main__":
    # This block won't produce actual microphone input without hardware/mocking
    # For a real demo, you'd need to pipe actual audio.
    # To run, ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    # For example:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    print("This script requires actual audio input to produce meaningful results.")
    print("Please ensure your microphone is working and GOOGLE_APPLICATION_CREDENTIALS is set.")
    # for transcript in stream_microphone_audio():
    #     pass # Process transcripts here
