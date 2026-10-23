from speech_client import get_speech_client
from google.cloud import speech_v1p1beta1 as speech

def submit_timestamped_transcription_job(gcs_uri: str, language_code: str = "en-US"):
    """Submits an audio file for batch transcription and returns word timestamps.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file.
        language_code: The language of the audio file.

    Returns:
        The long-running operation for the transcription job with word timestamps.
    """
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_word_time_offsets=True,
    )

    operation = client.longrunning_recognize(config=config, audio=audio)
    print(f"Timestamped transcription job submitted. Operation name: {operation.operation.name}")
    return operation

def get_timestamped_transcript_results(operation_name: str):
    """Retrieves and formats timestamped transcription results.

    Args:
        operation_name: The name of the long-running operation.

    Returns:
        A list of dictionaries containing word, start time, and end time.
    """
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    if operation.done:
        response = operation.result
        timestamps = []
        for result in response.results:
            for word_info in result.alternatives[0].words:
                timestamps.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                })
        return timestamps
    else:
        return None
