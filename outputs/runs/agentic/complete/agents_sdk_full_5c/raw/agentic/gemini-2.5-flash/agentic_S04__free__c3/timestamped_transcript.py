from speech_client import get_speech_client
from speech_models import create_word_timestamp_config, create_recognition_audio
from google.api_core.operation import Operation

def request_timestamped_transcript(gcs_uri: str, language_code: str = 'en-US') -> Operation:
    """Submits an audio file for batch transcription with word timestamps.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file.
        language_code: The BCP-47 language tag for the audio file.

    Returns:
        The long-running operation object for the timestamped transcription job.
    """
    client = get_speech_client()
    audio = create_recognition_audio(gcs_uri)
    config = create_word_timestamp_config(language_code=language_code, enable_word_time_offsets=True)

    print(f"Submitting timestamped transcription job for: {gcs_uri}...")
    operation = client.longrunning_recognize(config=config, audio=audio)
    print(f"Timestamped transcription job submitted. Operation name: {operation.operation.name}")
    return operation.operation

def get_timestamped_result(operation_name: str, timeout_seconds: int = 600) -> list:
    """Polls a timestamped transcription job and returns word-level timestamps.

    Args:
        operation_name: The name of the long-running operation.
        timeout_seconds: Maximum time to wait for the operation.

    Returns:
        A list of dictionaries, each containing 'word', 'startTime', 'endTime'.

    Raises:
        Exception: If the operation fails or times out.
    """
    client = get_speech_client()
    operation = Operation(operation_name, client)

    print(f"Polling timestamped results for: {operation_name}...")
    try:
        response = operation.result(timeout=timeout_seconds)

        word_timestamps = []
        for result in response.results:
            if result.alternatives and result.alternatives[0].words:
                for word_info in result.alternatives[0].words:
                    word_timestamps.append({
                        "word": word_info.word,
                        "startTime": f"{word_info.start_time.seconds}.{word_info.start_time.nanos // 1000000:03d}s",
                        "endTime": f"{word_info.end_time.seconds}.{word_time_info.nanos // 1000000:03d}s",
                    })
        print("Timestamped transcription job completed.")
        return word_timestamps

    except Exception as e:
        print(f"Timestamped transcription job failed or timed out: {e}")
        raise

# Example usage
# if __name__ == "__main__":
#     # audio_gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
#     # op = request_timestamped_transcript(audio_gcs_uri)
#     # # After some time, or in a separate script:
#     # # timestamps = get_timestamped_result(op.name)
#     # # for entry in timestamps:
#     # #     print(f"{entry['word']}: {entry['startTime']}-{entry['endTime']}")
#     pass
