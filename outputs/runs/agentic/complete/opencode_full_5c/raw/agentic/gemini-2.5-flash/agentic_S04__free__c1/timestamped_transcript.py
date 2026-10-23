import os
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.operation import Operation


def request_timestamped_transcript(
    gcs_uri: str, project_id: str, sample_rate_hertz: int, language_code: str
):
    """Requests a transcription with word-level timestamps.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file.
        project_id: The Google Cloud project ID.
        sample_rate_hertz: The sample rate of the audio in Hertz.
        language_code: The language code for the audio (e.g., "en-US").

    Returns:
        The operation name of the long-running transcription job.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name


def get_timestamped_transcript_result(operation_name: str):
    """Retrieves word or segment timestamps from a transcription result.

    Args:
        operation_name: The operation name of the long-running transcription job.

    Returns:
        A list of dictionaries, each containing word and its start/end times.
    """
    client = speech.SpeechClient()
    operation = Operation(name=operation_name, client=client)

    if operation.done():
        response = operation.result()
        word_timestamps = []
        for result in response.results:
            for word_info in result.alternatives[0].words:
                word_timestamps.append(
                    {
                        "word": word_info.word,
                        "start_time": word_info.start_time.seconds
                        + word_info.start_time.nanos * 1e-9,
                        "end_time": word_info.end_time.seconds
                        + word_info.end_time.nanos * 1e-9,
                    }
                )
        return word_timestamps
    return None


if __name__ == "__main__":
    # Example usage (replace with actual values)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    gcs_uri = "gs://cloud-samples-data/speech/flac/commercial_mono.flac"
    sample_rate_hertz = 16000
    language_code = "en-US"

    if project_id:
        print(f"Submitting timestamped transcription job for {gcs_uri}...")
        operation_name = request_timestamped_transcript(
            gcs_uri, project_id, sample_rate_hertz, language_code
        )
        print(
            f"Timestamped transcription job submitted. Operation Name: {operation_name}"
        )

        # In a real scenario, you would wait for the operation to complete
        # For demonstration, let's assume it completes quickly or use a dummy operation name
        # operation_name_for_retrieval = "projects/your-project-id/locations/global/operations/your-completed-operation-id"
        # print(f"Retrieving timestamped transcript for operation: {operation_name_for_retrieval}")
        # timestamps = get_timestamped_transcript_result(operation_name_for_retrieval)
        # if timestamps:
        #     for entry in timestamps:
        #         print(f"Word: {entry['word']}, Start: {entry['start_time']:.2f}s, End: {entry['end_time']:.2f}s")
        # else:
        #     print("Timestamped transcription job not yet complete or failed.")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
