import os
import assemblyai as aai

def transcribe_audio_file(audio_file_path: str) -> str:
    """
    Transcribes a synthesized audio file to verify its content using AssemblyAI.

    Args:
        audio_file_path: The local path to the audio file.

    Returns:
        The transcribed text, or an error message if transcription fails.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    aai.settings.api_key = api_key
    
    transcriber = aai.Transcriber()
    
    try:
        transcript = transcriber.transcribe(audio_file_path)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Transcription failed: {transcript.error}"
        
        return transcript.text or ""
        
    except Exception as e:
        return f"An error occurred during transcription: {e}"
