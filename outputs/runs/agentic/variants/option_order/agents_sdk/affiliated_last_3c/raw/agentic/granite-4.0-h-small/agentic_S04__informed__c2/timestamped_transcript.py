import os
import assemblyai as aai
import json

def timestamped_transcription(audio_path: str) -> str:
    """Submit a batch transcription job with word timestamps.
    Returns a JSON string containing the timestamped transcript.
    """
    response = client.transcribe(
        audio_url=audio_path,
        format="json",
        boost_performance=True,
    )
    job_id = response["id"]
    status = client.check_transcription(job_id)
    while status["status"] not in ("completed", "error"):
        time.sleep(5)
        status = client.check_transcription(job_id)
    if status["status"] == "error":
        raise RuntimeError(f"Timestamp transcription failed: {status.get('error')}")
    result = client.download_transcript(job_id, format="json")
    # Convert to pretty JSON
    return json.dumps(result, indent=2)
