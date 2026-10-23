from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError
from speech_client import get_speech_client
from speech_models import TimestampedTranscriptResponse

def timestamped_transcript(job_id: str) -> TimestampedTranscriptResponse:
    """
    Returns word or segment timestamps from a Google Cloud Speech-to-Text transcription result.
    """
    client = get_speech_client()

    try:
        operation = client.transport._operations_client.get_operation(job_id)
        if not operation.done:
            return TimestampedTranscriptResponse(
                job_id=job_id,
                status="PROCESSING",
                segments=None,
                error=None
            )

        if operation.response:
            segments = []
            for result in operation.response.results:
                for word_info in result.alternatives[0].words:
                    segments.append({
                        "word": word_info.word,
                        "start_time": word_info.start_time.total_seconds(),
                        "end_time": word_info.end_time.total_seconds(),
                    })
            return TimestampedTranscriptResponse(
                job_id=job_id,
                status="COMPLETED",
                segments=segments,
                error=None
            )
        else:
            return TimestampedTranscriptResponse(
                job_id=job_id,
                status="FAILED",
                segments=None,
                error="No timestamped results returned"
            )
    except GoogleAPICallError as e:
        return TimestampedTranscriptResponse(
            job_id=job_id,
            status="FAILED",
            segments=None,
            error=str(e)
        )