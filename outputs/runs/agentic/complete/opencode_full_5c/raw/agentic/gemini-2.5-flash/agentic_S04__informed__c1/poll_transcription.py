import time
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionResult


def poll_transcription_job(operation_id: str) -> TranscriptionResult:
    """Polls a Google Cloud Speech-to-Text transcription job and returns the transcript.

    Args:
        operation_id: The ID of the long-running operation.

    Returns:
        A TranscriptionResult object containing the job status and transcript.
    """
    client = get_speech_client()
    operation_name = f"projects/-/locations/global/operations/{operation_id}"
    operation = client.get_operation(name=operation_name)

    while not operation.done:
        print("Transcription job is still in progress... Waiting 30 seconds.")
        time.sleep(30)
        operation = client.get_operation(name=operation_name)

    if operation.error:
        status = "FAILED"
        transcript = f"Error: {operation.error.message}"
    else:
        status = "COMPLETED"
        response = operation.result
        transcript_parts = []
        word_timestamps = []
        speaker_diarization = []

        for result in response.results:
            if result.alternatives:
                best_alternative = result.alternatives[0]
                transcript_parts.append(best_alternative.transcript)
                if best_alternative.words:
                    for word_info in best_alternative.words:
                        word_timestamps.append(
                            {
                                "word": word_info.word,
                                "start_time": word_info.start_time.seconds
                                + word_info.start_time.nanos * 1e-9,
                                "end_time": word_info.end_time.seconds
                                + word_info.end_time.nanos * 1e-9,
                                "speaker_tag": word_info.speaker_tag
                                if hasattr(word_info, "speaker_tag")
                                else None,
                            }
                        )
                # Google Cloud Speech-to-Text often includes speaker tags directly in word info for diarization
                # For a more structured diarization output, one might need to re-process word_timestamps

        transcript = " ".join(transcript_parts)

    return TranscriptionResult(
        job_name=operation_id,
        status=status,
        transcript=transcript,
        word_timestamps=word_timestamps if word_timestamps else None,
        diarization_speakers=None,  # Placeholder, as speaker info is usually in word_timestamps
    )
