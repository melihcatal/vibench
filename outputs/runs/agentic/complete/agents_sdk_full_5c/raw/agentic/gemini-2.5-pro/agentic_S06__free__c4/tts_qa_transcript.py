"""
Transcribe synthesized QA samples to verify spoken output using AssemblyAI.
"""
from speech_client import get_assemblyai_transcriber
from speech_models import TranscriptionResponse
import assemblyai

def transcribe_audio_file_assemblyai(audio_path: str) -> TranscriptionResponse:
    """
    Transcribes an audio file using AssemblyAI to verify TTS output.

    Args:
        audio_path: The local path to the audio file (e.g., a synthesized .mp3).

    Returns:
        A TranscriptionResponse object with the transcribed text.
    """
    transcriber = get_assemblyai_transcriber()
    
    config = assemblyai.TranscriptionConfig(speaker_labels=False)

    transcript = transcriber.transcribe(audio_path, config=config)

    if transcript.status == assemblyai.TranscriptStatus.error:
        raise ConnectionError(f"AssemblyAI transcription failed: {transcript.error}")

    return TranscriptionResponse(
        text=transcript.text,
        confidence=transcript.confidence
    )
