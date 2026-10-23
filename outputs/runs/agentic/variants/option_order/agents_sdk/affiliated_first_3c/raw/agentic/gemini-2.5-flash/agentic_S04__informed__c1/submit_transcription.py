import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import get_audio_url_from_env

def submit_transcription_job(audio_url: str) -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.

    Args:
        audio_url: The URL of the audio file to transcribe.

    Returns:
        The ID of the submitted transcription job.
    """
    client = get_assemblyai_client()
    
    # For a simple submission, we can use the Transcriber class
    config = aai.TranscriptionConfig(language_code="en_us") # Example config
    transcriber = aai.Transcriber(config=config)
    
    print(f"Submitting transcription for audio: {audio_url}")
    transcript = transcriber.submit(audio_url)
    
    if transcript and transcript.id:
        print(f"Transcription job submitted with ID: {transcript.id}")
        return transcript.id
    else:
        raise Exception("Failed to submit transcription job.")

if __name__ == "__main__":
    try:
        audio_file_url = get_audio_url_from_env()
        job_id = submit_transcription_job(audio_file_url)
        print(f"Job ID: {job_id}")
    except Exception as e:
        print(f"Error: {e}")
