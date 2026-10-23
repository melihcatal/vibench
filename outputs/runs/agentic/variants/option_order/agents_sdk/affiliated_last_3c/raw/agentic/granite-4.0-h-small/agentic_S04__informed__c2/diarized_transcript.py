import os
import assemblyai as aai

# Provide your API key as an environment variable
client = aai.TranscriptionClient(api_key=os.getenv("ASSEMBLYAI_API_KEY"))

def diarized_transcription(audio_path: str) -> str:
    """Submit a batch transcription job with speaker diarization.
    AssemblyAI supports up to four speakers.
    Returns the diarized transcript text.
    """
    transcript = client.transcribe(
        audio_url=audio_path,
        speakers=4,  # adjust as needed
        format="txt",
        boost_performance=True,
    )
    job_id = transcript["id"]
    # Wait for completion
    status = client.check_transcription(job_id)
    while status["status"] not in ("completed", "error"):
        time.sleep(5)
        status = client.check_transcription(job_id)
    if status["status"] == "error":
        raise RuntimeError(f"Diarization failed: {status.get('error')}")
    result = client.download_transcript(job_id)
    return result["text"]
