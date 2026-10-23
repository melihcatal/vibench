import time

from speech_client import SpeechClient
from speech_models import TranscriptionJobResult


def poll_transcription(job_id: str, config=None):
    config = config or {}
    client = SpeechClient(region_name=config.get("region")).get_transcribe_client()

    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_id)
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        print(f"Transcription job {job_id} status: {job_status}")

        if job_status in ["COMPLETED", "FAILED"]:
            transcript_uri = None
            if job_status == "COMPLETED":
                transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            
            return TranscriptionJobResult(
                job_id=job_id,
                status=job_status,
                transcript_uri=transcript_uri,
                language_code=response["TranscriptionJob"]["LanguageCode"],
                creation_time=str(response["TranscriptionJob"]["CreationTime"]),
                completion_time=str(response["TranscriptionJob"]["CompletionTime"]),
                failure_reason=response["TranscriptionJob"].get("FailureReason"),
            )
        
        time.sleep(5)  # Wait for 5 seconds before polling again
