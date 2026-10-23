from speech_client import get_speech_client

def poll_transcription_job(operation_name: str):
    """Polls a transcription job and returns the transcript.

    Args:
        operation_name: The name of the long-running operation.

    Returns:
        The transcription result if the operation is complete, otherwise None.
    """
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    if operation.done:
        response = operation.result
        transcript = "".join([result.alternatives[0].transcript for result in response.results])
        print("Transcription complete.")
        return transcript
    else:
        print("Transcription job still in progress.")
        return None
