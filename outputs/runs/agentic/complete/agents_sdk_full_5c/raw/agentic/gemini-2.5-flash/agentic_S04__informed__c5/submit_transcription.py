import os
import assemblyai

def submit_transcription_job(audio_url: str) -> assemblyai.Transcript:
    """Submits an audio file for batch transcription to AssemblyAI."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = assemblyai.Transcriber(api_key)
    config = assemblyai.TranscriptionConfig(audio_url=audio_url)
    
    # Submit the transcription job
    transcript = transcriber.transcribe(config)
    return transcript
