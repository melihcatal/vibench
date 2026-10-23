
import os
from google.cloud import speech_to_text

def transcribe_with_word_time_offsets(audio_file_path: str):
    """Transcribe the given audio file synchronously and include word time offsets."""
    client = speech_to_text.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech_to_text.RecognitionAudio(content=content)
    config = speech_to_text.RecognitionConfig(
        encoding=speech_to_text.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
        print("Word details:")
        for word in result.alternatives[0].words:
            print(f"    Word: {word.word}")
            print(f"    Start time: {word.start_time.seconds + word.start_time.nanos * 1e-9}s")
            print(f"    End time: {word.end_time.seconds + word.end_time.nanos * 1e-9}s")

if __name__ == "__main__":
    # Example usage: Replace 'path/to/your/audio.wav' with your audio file path
    # Make sure to set up Google Cloud authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # For more info: https://cloud.google.com/docs/authentication/getting-started
    # transcribe_with_word_time_offsets("path/to/your/audio.wav")
    pass
