from speech_client import get_speech_client
from speech_models import create_diarization_config, create_recognition_audio
from google.api_core.operation import Operation

def request_diarized_transcript(gcs_uri: str, language_code: str = 'en-US', 
                                min_speaker_count: int = 2, max_speaker_count: int = 6) -> Operation:
    """Submits an audio file for batch transcription with speaker diarization.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file.
        language_code: The BCP-47 language tag for the audio file.
        min_speaker_count: The minimum number of speakers in the audio clip.
        max_speaker_count: The maximum number of speakers in the audio clip.

    Returns:
        The long-running operation object for the diarization job.
    """
    client = get_speech_client()
    audio = create_recognition_audio(gcs_uri)
    config = create_diarization_config(
        language_code=language_code,
        min_speaker_count=min_speaker_count,
        max_speaker_count=max_speaker_count,
    )

    print(f"Submitting diarization job for: {gcs_uri}...")
    operation = client.longrunning_recognize(config=config, audio=audio)
    print(f"Diarization job submitted. Operation name: {operation.operation.name}")
    return operation.operation

def get_diarized_result(operation_name: str, timeout_seconds: int = 600) -> list:
    """Polls a diarization job and returns a list of diarized segments.

    Args:
        operation_name: The name of the long-running operation.
        timeout_seconds: Maximum time to wait for the operation.

    Returns:
        A list of dictionaries, each containing 'speakerTag', 'word', 'startTime', 'endTime'.

    Raises:
        Exception: If the operation fails or times out.
    """
    client = get_speech_client()
    operation = Operation(operation_name, client)

    print(f"Polling diarization results for: {operation_name}...")
    try:
        response = operation.result(timeout=timeout_seconds)

        diarized_segments = []
        for result in response.results:
            for word_info in result.alternatives[0].words:
                diarized_segments.append({
                    "speakerTag": word_info.speaker_tag,
                    "word": word_info.word,
                    "startTime": f"{word_info.start_time.seconds}.{word_info.start_time.nanos // 1000000:03d}s",
                    "endTime": f"{word_info.end_time.seconds}.{word_info.end_time.nanos // 1000000:03d}s",
                })
        print("Diarization job completed.")
        return diarized_segments

    except Exception as e:
        print(f"Diarization job failed or timed out: {e}")
        raise

# Example usage
# if __name__ == "__main__":
#     # audio_gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
#     # op = request_diarized_transcript(audio_gcs_uri)
#     # # After some time, or in a separate script:
#     # # diarized_output = get_diarized_result(op.name)
#     # # for segment in diarized_output:
#     # #     print(f"[Speaker {segment['speakerTag']}] {segment['startTime']}-{segment['endTime']}: {segment['word']}")
#     pass
