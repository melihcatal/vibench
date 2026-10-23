from google.cloud import speech_v1p1beta1 as speech

def poll_transcription_job(operation_name: str) -> str:
    """Polls a transcription job and returns the transcript.

    Args:
        operation_name: The name of the long-running operation for the transcription job.

    Returns:
        The full transcript as a string.
    """
    client = speech.SpeechClient()

    operation = client.get_operation(name=operation_name)

    # Blocks until the operation is complete.
    response = operation.result()

    transcript_builder = []
    for result in response.results:
        transcript_builder.append(result.alternatives[0].transcript)

    return " ".join(transcript_builder)
