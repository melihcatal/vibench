import os
import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionConfig

def submit_transcription_job(config: TranscriptionConfig) -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    Returns the job ID.
    """
    client = get_assemblyai_client()
    
    config_params = {}
    if config.diarization_enabled:
        config_params["speaker_labels"] = True
    if config.word_timestamps_enabled:
        config_params["word_boost"] = [] # Placeholder to enable word-level details
        config_params["auto_chapters"] = False # Ensure not to conflict with basic timestamps
    
    transcriber = aai.Transcriber()
    
    # AssemblyAI's SDK handles various inputs, passing audio_url directly.
    # The SDK automatically starts the transcription when you call .transcribe() or .submit()
    # For a batch job and getting an ID to poll, we usually create a real-time transcript or submit.
    # The client.transcribe_url function handles submission and polling automatically.
    # To get a job ID for separate polling, we use a more explicit submission.

    # Example using aai.Transcription for explicit job creation
    transcript_object = transcriber.submit(
        audio=config.audio_url,
        config=aai.TranscriptionConfig(**config_params)
    )
    
    return transcript_object.id

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    audio_url = "https://example.com/audio.mp3" # Use a public audio URL for testing
    
    # Ensure ASSEMBLYAI_API_KEY is set in your environment
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    else:
        config = TranscriptionConfig(audio_url=audio_url)
        job_id = submit_transcription_job(config)
        print(f"Submitted transcription job with ID: {job_id}")
