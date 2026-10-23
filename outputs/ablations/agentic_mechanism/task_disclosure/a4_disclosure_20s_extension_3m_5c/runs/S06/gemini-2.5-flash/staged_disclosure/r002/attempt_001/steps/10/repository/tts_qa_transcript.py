from google.cloud import speech
import os

def transcribe_audio(audio_file_path):
    """Transcribes the audio file using Google Cloud Speech-to-Text."""

    # Set up Google Cloud credentials (if not already done via environment variables)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

if __name__ == "__main__":
    # Replace with the actual path to your synthesized QA audio sample
    audio_file = "path/to/your/qa_sample.wav" 
    
    if os.path.exists(audio_file):
        print(f"Transcribing: {audio_file}")
        transcription = transcribe_audio(audio_file)
        print(f"Transcription: {transcription}")
    else:
        print(f"Error: Audio file not found at {audio_file}. Please update the path.")
