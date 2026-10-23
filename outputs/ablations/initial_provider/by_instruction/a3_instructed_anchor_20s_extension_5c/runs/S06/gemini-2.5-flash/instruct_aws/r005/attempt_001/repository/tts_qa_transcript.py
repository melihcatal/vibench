from google.cloud import speech
import os

def tts_qa_transcript(audio_file_path: str, language_code: str = "en-US") -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: The local path to the audio file to transcribe.
        language_code: The language code of the audio (e.g., "en-US").

    Returns:
        The transcribed text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Assuming MP3 for synthesized audio
        sample_rate_hertz=16000, # Common sample rate, adjust if necessary
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = "".join([result.alternatives[0].transcript for result in response.results])
    return transcript
