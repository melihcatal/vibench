from google.cloud import speech_v1p1beta1 as speech
from google.api_core.operation import Operation

def poll_transcription_job(operation_name: str) -> str:
    """Polls a transcription job and returns the transcript.

    Args:
        operation_name: The name of the long-running operation (job ID).

    Returns:
        The transcribed text if the job is completed, otherwise an empty string.
    """
    client = speech.SpeechClient()

    operation: Operation = client.long_running_recognize(
        operation_name=operation_name
    )

    result = operation.result()

    transcript_parts = []
    for result in result.results:
        for alternative in result.alternatives:
            transcript_parts.append(alternative.transcript)

    return " ".join(transcript_parts)
