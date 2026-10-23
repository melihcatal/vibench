import os
import assemblyai as aai

def transcribe_audio_from_url(audio_url: str) -> str:
    aai_api_key = os.environ.get("ASSEMBLYAI_API_KEY")

    if not aai_api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    aai.settings.api_key = aai_api_key

    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(
        language_code="en_us", # Specify language if known
    )

    transcript = transcriber.transcribe(audio_url, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"AssemblyAI Transcription Error: {transcript.error}")
    else:
        return transcript.text
