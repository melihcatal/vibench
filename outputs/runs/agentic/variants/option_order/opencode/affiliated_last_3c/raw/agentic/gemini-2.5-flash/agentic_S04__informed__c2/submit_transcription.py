import os
import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def submit_transcription_job(audio_url: str) -> aai.Transcript:
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(language_code="en_us")
    transcript = transcriber.submit(audio_url, config)
    return transcript
