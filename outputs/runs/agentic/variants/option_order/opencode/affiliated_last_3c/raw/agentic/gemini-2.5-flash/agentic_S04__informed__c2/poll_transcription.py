import os
import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def poll_transcription_job(transcript_id: str) -> aai.Transcript:
    transcriber = aai.Transcriber()
    transcript = transcriber.wait_until_ready(transcript_id)
    return transcript
