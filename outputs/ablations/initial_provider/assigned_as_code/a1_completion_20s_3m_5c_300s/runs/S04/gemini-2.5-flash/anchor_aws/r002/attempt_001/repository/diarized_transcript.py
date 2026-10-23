import boto3
from speech_client import SpeechClient
from speech_models import DiarizationRequest, TranscriptionJobResult


def diarized_transcript(request: DiarizationRequest, config=None) -> TranscriptionJobResult:
    config = config or {}
    client = SpeechClient(region_name=config.get("region")).get_transcribe_client()

    # In a real scenario, the transcription job must have been started with speaker diarization enabled.
    # For this example, we assume the job with job_id already exists and has diarization enabled.
    response = client.get_transcription_job(TranscriptionJobName=request.job_id)
    job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]

    if job_status == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        # In a real application, you would download and parse the JSON from this URI.
        # The parsed JSON would contain speaker labels if diarization was enabled.
        # For demonstration, we'll return a simplified structure.
        return TranscriptionJobResult(
            job_id=request.job_id,
            status=job_status,
            transcript_uri=transcript_uri,
            language_code=response["TranscriptionJob"]["LanguageCode"],
            creation_time=str(response["TranscriptionJob"]["CreationTime"]),
            completion_time=str(response["TranscriptionJob"]["CompletionTime"]),
        )
    elif job_status == "FAILED":
        raise Exception(f"Transcription job {request.job_id} failed: {response['TranscriptionJob'].get('FailureReason')}")
    else:
        raise Exception(f"Transcription job {request.job_id} is not yet completed. Current status: {job_status}")
