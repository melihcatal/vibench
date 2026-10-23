
from google.cloud import speech_v1p1beta1 as speech

def get_timestamped_transcript(operation_result):
    """
    Extracts word or segment timestamps from a Google Cloud Speech-to-Text transcription result.

    Args:
        operation_result: The result object from a Google Cloud Speech-to-Text long-running operation.

    Returns:
        A list of dictionaries, where each dictionary represents a word or segment
        with its start time, end time, and word/segment content.
    """
    timestamps = []
    for result in operation_result.results:
        for alternative in result.alternatives:
            if alternative.words:
                for word_info in alternative.words:
                    timestamps.append({
                        "word": word_info.word,
                        "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                        "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                        "type": "word"
                    })
            else:
                # If word-level timestamps are not available, try to get segment-level (result level)
                timestamps.append({
                    "transcript": alternative.transcript,
                    "type": "segment"
                })
    return timestamps

