from google.cloud import speech_v1p1beta1 as speech
import os

def get_timestamped_transcript(operation_name: str):
    """Returns word or segment timestamps from a completed transcription result.

    Args:
        operation_name: The name of the long-running operation for the transcription.

    Returns:
        A list of dictionaries, each containing word, start time, and end time.
        Returns None if the operation is not yet complete.
    """
    client = speech.SpeechClient()
    operation = client.operations_client.get_operation(name=operation_name)

    if operation.done:
        response = speech.LongRunningRecognizeResponse(operation.response)
        word_timestamps = []
        for result in response.results:
            for word_info in result.alternatives[0].words:
                word_timestamps.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                    "speaker_tag": word_info.speaker_tag if hasattr(word_info, 'speaker_tag') else None # For diarized transcripts
                })
        print("Transcription with timestamps complete.")
        return word_timestamps
    else:
        print("Transcription job is still in progress.")
        return None

if __name__ == '__main__':
    # Example usage (replace with your actual operation name)
    OPERATION_NAME = os.getenv("TRANSCRIPTION_OPERATION_NAME", "projects/your-gcp-project-id/locations/global/operations/your-operation-id")

    if "your-operation-id" in OPERATION_NAME:
        print("Please set the TRANSCRIPTION_OPERATION_NAME environment variable or replace 'your-operation-id' with an actual operation ID.")
    else:
        print(f"Retrieving timestamps for operation: {OPERATION_NAME}")
        timestamps = None
        # In a real scenario, you'd poll until done or ensure the operation is complete
        # For this example, we assume it's already done or will retrieve if it is.
        timestamps = get_timestamped_transcript(OPERATION_NAME)
        if timestamps:
            for ts in timestamps:
                print(f"Word: {ts['word']}, Start: {ts['start_time']:.2f}s, End: {ts['end_time']:.2f}s, Speaker: {ts['speaker_tag']}")
