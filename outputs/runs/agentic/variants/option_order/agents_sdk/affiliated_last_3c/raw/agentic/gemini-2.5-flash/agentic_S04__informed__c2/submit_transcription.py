import os
import assemblyai as aai

def submit_transcription_job(audio_url: str) -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.

    Args:
        audio_url: The URL of the audio file to transcribe.

    Returns:
        The ID of the submitted transcription job.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(language_code="en_us")
    transcript = transcriber.submit(audio_url, config=config)
    return transcript.id

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # job_id = submit_transcription_job("https://example.com/audio.mp3")
    # print(f"Submitted transcription job with ID: {job_id}")
    pass