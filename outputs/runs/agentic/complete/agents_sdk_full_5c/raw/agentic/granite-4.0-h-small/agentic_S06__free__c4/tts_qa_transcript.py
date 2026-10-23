import os
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

def transcribe_audio(audio_path: str, sample_rate_hertz: int = 24000):
    """Transcribe a synthesized audio file using Google Speech-to-Text."""
    audio = speech.RecognitionAudio(uri=f"gs://{os.getenv('GCS_BUCKET')}/{audio_path}")
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=sample_rate_hertz,
        language_code="en-US",
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    result = operation.result(timeout=180)
    transcript = result.results[0].alternatives[0].transcript
    print(f"Transcript: {transcript}")
    return transcript

if __name__ == "__main__":
    # Example usage (requires GCS_BUCKET env var set and audio file uploaded)
    audio_file = "output.ogg"
    transcribe_audio(audio_file)
