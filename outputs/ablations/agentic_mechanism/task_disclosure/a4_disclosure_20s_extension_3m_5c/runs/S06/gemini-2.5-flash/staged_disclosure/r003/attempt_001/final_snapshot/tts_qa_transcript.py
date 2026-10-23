import os
from google.cloud import speech

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes an audio file using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: The path to the audio file to transcribe.

    Returns:
        The transcribed text.
    """
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio file into memory
    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000, # Adjust if your audio has a different sample rate
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

if __name__ == "__main__":
    # This is a placeholder for your audio file.
    # Replace with the actual path to your synthesized QA audio sample.
    audio_sample_path = "path/to/your/qa_sample.wav"

    if os.path.exists(audio_sample_path):
        print(f"Transcribing: {audio_sample_path}")
        transcribed_text = transcribe_audio(audio_sample_path)
        print("Transcription:")
        print(transcribed_text)
    else:
        print(f"Error: Audio file not found at {audio_sample_path}")
        print("Please replace 'path/to/your/qa_sample.wav' with the actual path to your audio file.")
        print("Also ensure you have set up Google Cloud authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable).")
