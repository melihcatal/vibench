import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_qa_audio_sample(audio_bytes: bytes, language_code: str = "en-US") -> str:
    """Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.

    Args:
        audio_bytes: The audio content as bytes.
        language_code: The BCP-47 language code of the audio (e.g., "en-US").

    Returns:
        The transcribed text, or an empty string if transcription fails.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Assuming MP3 output from TTS
        sample_rate_hertz=16000, # Common sample rate, adjust if TTS output differs
        language_code=language_code,
    )

    try:
        response = client.recognize(config=config, audio=audio)
        if response.results:
            return response.results[0].alternatives[0].transcript
        return ""
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
