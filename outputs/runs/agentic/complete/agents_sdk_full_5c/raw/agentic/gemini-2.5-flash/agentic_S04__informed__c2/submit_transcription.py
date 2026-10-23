import os
import assemblyai as aai
from speech_models import TranscriptionRequest

def submit_transcription(audio_url: str) -> str:
    """Submits an audio file for batch transcription using AssemblyAI."""
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    config = aai.TranscriptionConfig(
        speaker_labels=False,
        punctuate=True,
        format_text=True
    )
    
    transcriber = aai.Transcriber()
    transcript = transcriber.submit_for_transcription(audio_url, config)
    
    return transcript.id

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # audio_file_url = "https://example.com/audio.mp3"
    # job_id = submit_transcription(audio_file_url)
    # print(f"Submitted transcription job with ID: {job_id}")
    pass
