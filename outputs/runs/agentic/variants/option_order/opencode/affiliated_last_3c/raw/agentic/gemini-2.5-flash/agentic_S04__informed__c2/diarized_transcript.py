import os
import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def get_diarized_transcript(audio_url: str) -> aai.Transcript:
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_diarization=True, language_code="en_us")
    transcript = transcriber.transcribe(audio_url, config)
    return transcript
