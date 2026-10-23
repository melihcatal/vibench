import os
import assemblyai

def request_diarized_transcript(audio_url: str) -> assemblyai.Transcript:
    """Submits an audio file for transcription with speaker diarization to AssemblyAI."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = assemblyai.Transcriber(api_key)
    config = assemblyai.TranscriptionConfig(
        audio_url=audio_url,
        speaker_diarization=True
    )
    
    transcript = transcriber.transcribe(config)
    return transcript
