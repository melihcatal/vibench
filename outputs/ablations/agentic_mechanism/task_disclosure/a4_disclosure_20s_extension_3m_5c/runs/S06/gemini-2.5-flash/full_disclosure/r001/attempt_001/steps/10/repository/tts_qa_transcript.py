from google.cloud import speech

def transcribe_audio(audio_file_path: str, project_id: str) -> str:
    """Transcribes an audio file using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: Path to the audio file to transcribe.
        project_id: Your Google Cloud project ID.

    Returns:
        The transcribed text.
    """

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
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()

if __name__ == "__main__":
    # Replace with your audio file path and Google Cloud project ID
    audio_file = "path/to/your/audio.wav"
    gcp_project_id = "your-gcp-project-id"

    # Example usage:
    # transcribed_text = transcribe_audio(audio_file, gcp_project_id)
    # print(f"Transcribed text: {transcribed_text}")
