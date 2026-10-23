import os
import assemblyai as aai

# Configure client using environment variable
client = aai.TranscriptionClient(
    api_key=os.getenv("ASSEMBLYAI_API_KEY")
)

def submit_transcription(audio_path: str, speakers: int = 1) -> str:
    """Submit a batch transcription job for the given audio file.
    Returns the job ID.
    """
    # AssemblyAI supports up to four speakers for diarization
    response = client.transcribe(
        audio_url=audio_path,
        speakers=speakers,
        format="txt",
        boost_performance=True,
    )
    job_id = response["id"]
    return job_id
