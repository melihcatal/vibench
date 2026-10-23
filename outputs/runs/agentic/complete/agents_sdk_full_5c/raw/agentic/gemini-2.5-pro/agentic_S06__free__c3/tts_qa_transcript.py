import os
import assemblyai as aai

def transcribe_audio_file(audio_path: str) -> str:
    """
    Transcribes a synthesized audio file to text for verification using AssemblyAI.

    Requires the ASSEMBLYAI_API_KEY environment variable to be set.

    Args:
        audio_path: The local path to the audio file to be transcribed.

    Returns:
        The transcribed text.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
        
    aai.settings.api_key = api_key

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        return f"Transcription failed: {transcript.error}"
    
    if transcript.text is None:
        return ""
        
    return transcript.text
