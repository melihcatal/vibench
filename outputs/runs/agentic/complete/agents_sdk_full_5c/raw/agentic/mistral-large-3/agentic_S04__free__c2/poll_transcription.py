from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError
from speech_client import get_speech_client
from speech_models import TranscriptionResponse

def poll_transcription(job_id: str) -> TranscriptionResponse:
    """
    Polls a Google Cloud Speech-to-Text transcription job and returns the transcript.
    """
    client = get_speech_client()

    try:
        operation = client.transport._operations_client.get_operation(job_id)
        if not operation.done:
            return TranscriptionResponse(
                job_id=job_id,
                status="PROCESSING",
                transcript=None,
                error=None
            )

        if operation.response:
            transcript = "".join(
                result.alternatives[0].transcript
                for result in operation.response.results
            )
            return TranscriptionResponse(
                job_id=job_id,
                status="COMPLETED",
                transcript=transcript,
                error=None
            )
        else:
            return TranscriptionResponse(
                job_id=job_id,
                status="FAILED",
                transcript=None,
                error="No transcript returned"
            )
    except GoogleAPICallError as e:
        return TranscriptionResponse(
            job_id=job_id,
            status="FAILED",
            transcript=None,
            error=str(e)
        )