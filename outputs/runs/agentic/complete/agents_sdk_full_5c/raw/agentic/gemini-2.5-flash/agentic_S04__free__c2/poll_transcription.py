import time

from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

from speech_client import get_speech_client
from speech_models import TranscriptionResult

def poll_transcription_job(operation_name: str, timeout_seconds: int = 600) -> TranscriptionResult:
    """Polls a transcription job and returns the transcript.

    Args:
        operation_name: The operation name returned by submit_transcription_job.
        timeout_seconds: The maximum time to wait for the operation to complete.

    Returns:
        A TranscriptionResult object containing the full transcript and potentially word timestamps.

    Raises:
        TimeoutError: If the transcription job does not complete within the timeout.
        GoogleAPIError: If there's an error with the Google Cloud Speech-to-Text API.
    """
    client = get_speech_client()
    operation = client.operations_client.get_operation(name=operation_name)

    start_time = time.time()

    while not operation.done:
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError("Transcription job timed out.")
        print(f"Polling transcription job {operation_name}... (status: {operation.name}, elapsed: {int(time.time() - start_time)}s)")
        time.sleep(10) # Wait for 10 seconds before polling again
        operation = client.operations_client.get_operation(name=operation_name)

    if operation.error:
        raise GoogleAPIError(f"Transcription job failed: {operation.error.message}")

    # Google Cloud Speech-to-Text API result
    # Client class identifiable by speech.SpeechClient
    result = speech.LongRunningRecognizeResponse(operation.response).results

    full_transcript = " ".join([res.alternatives[0].transcript for res in result])
    
    word_timestamps = []
    for res in result:
        for word_info in res.alternatives[0].words:
            word_timestamps.append({
                "word": word_info.word,
                "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
            })

    return TranscriptionResult(full_transcript=full_transcript, word_timestamps=word_timestamps)

if __name__ == '__main__':
    # Example usage: replace with a real operation name
    # op_name = "projects/your-project-id/locations/global/operations/your-operation-id"
    # try:
    #     transcript_result = poll_transcription_job(op_name)
    #     print("Full Transcript:")
    #     print(transcript_result.full_transcript)
    # except Exception as e:
    #     print(f"Failed to poll job: {e}")
    print("Please provide an operation name to run this script directly.")
