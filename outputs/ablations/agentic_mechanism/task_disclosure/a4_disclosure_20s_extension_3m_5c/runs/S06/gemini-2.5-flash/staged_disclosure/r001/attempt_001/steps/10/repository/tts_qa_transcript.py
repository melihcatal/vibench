from google.cloud import speech

def transcribe_audio(audio_file_path):
    """Transcribes the given audio file using Google Cloud Speech-to-Text."""
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

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    return " ".join(transcripts)

if __name__ == "__main__":
    # Replace with your actual synthesized QA audio file path
    # Example: "path/to/your/qa_sample.wav"
    audio_file = "path/to/your/synthesized_qa_sample.wav" 
    
    # NOTE: Ensure you have authenticated to Google Cloud and enabled the Speech-to-Text API.
    # For authentication, you can set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    print(f"Transcribing audio from: {audio_file}")
    transcribed_text = transcribe_audio(audio_file)
    print("Transcription:")
    print(transcribed_text)
