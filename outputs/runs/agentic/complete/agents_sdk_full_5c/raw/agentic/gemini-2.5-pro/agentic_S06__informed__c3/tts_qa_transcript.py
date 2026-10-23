import os
import assemblyai

def transcribe_audio_file(audio_file_path: str) -> str:
    """
    Transcribes a synthesized audio file for QA using AssemblyAI.
    Expects ASSEMBLYAI_API_KEY environment variable.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    assemblyai.settings.api_key = api_key
    transcriber = assemblyai.Transcriber()

    transcript = transcriber.transcribe(audio_file_path)

    if transcript.status == assemblyai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")
    
    return transcript.text
