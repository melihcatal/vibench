import os
import assemblyai as aai


def transcribe_audio(audio_url: str) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using AssemblyAI.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url)
    return transcript.text
