import os
import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def get_timestamped_transcript(audio_url: str) -> aai.Transcript:
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(
        word_boost=["hello", "world"], language_code="en_us"
    )
    transcript = transcriber.transcribe(audio_url, config)
    return transcript
