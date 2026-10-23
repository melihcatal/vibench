from google.cloud import speech

def transcribe_audio_sample(audio_file_path: str) -> str:
    """Transcribes synthesized QA audio samples to verify spoken output using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: The path to the audio file to transcribe.

    Returns:
        The transcribed text from the audio file.
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
        transcript += result.alternatives[0].transcript
    return transcript
