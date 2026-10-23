from google.cloud import speech

def transcribe_audio(audio_file_path: str, sample_rate_hertz: int, language_code: str = "en-US"):
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: The path to the audio file to transcribe.
        sample_rate_hertz: The sample rate of the audio file in Hertz.
        language_code: The language code of the audio (e.g., "en-US", "es-ES").

    Returns:
        The transcription of the audio file.
    """
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript
