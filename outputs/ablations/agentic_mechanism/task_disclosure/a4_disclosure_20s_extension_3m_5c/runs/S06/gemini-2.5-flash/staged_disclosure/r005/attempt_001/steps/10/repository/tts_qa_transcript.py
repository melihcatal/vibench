from google.cloud import speech

def transcribe_audio(audio_file_path: str) -> str:
    """Transcribes an audio file using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: The path to the audio file to transcribe.

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
        model="default",  # Using a default model, can be changed to specific ones like "phone_call" or "video"
    )

    response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)

if __name__ == "__main__":
    # Example usage (replace with actual audio file)
    # For a real scenario, you would have synthesized QA audio files here.
    # For demonstration, let's assume you have an audio file named "sample_qa.wav"
    # To run this, you would need to install the google-cloud-speech library:
    # pip install google-cloud-speech
    # And set up Google Cloud authentication.
    
    # You can create a dummy audio file for testing, or use a real one.
    # For example, create a simple 16-bit, 16kHz mono WAV file.
    
    # print("Please make sure you have a 'sample_qa.wav' file in the same directory.")
    # audio_path = "sample_qa.wav"
    # try:
    #     transcribed_text = transcribe_audio(audio_path)
    #     print(f"Transcribed text: {transcribed_text}")
    # except FileNotFoundError:
    #     print(f"Error: The audio file '{audio_path}' was not found.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    pass
