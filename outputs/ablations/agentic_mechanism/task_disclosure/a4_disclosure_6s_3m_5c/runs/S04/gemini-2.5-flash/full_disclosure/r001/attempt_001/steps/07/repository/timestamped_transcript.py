from google.cloud import speech_v1p1beta1 as speech

def get_word_timestamps(transcript_result: dict) -> list[dict]:
    """
    Extracts word-level timestamps from a Google Cloud Speech-to-Text transcription result.

    Args:
        transcript_result: A dictionary representing the JSON response from
                           Google Cloud Speech-to-Text with word time offsets enabled.

    Returns:
        A list of dictionaries, where each dictionary contains 'word', 'start_time',
        and 'end_time' for each word in the transcript.
    """
    word_timestamps = []
    if "results" in transcript_result:
        for result in transcript_result["results"]:
            if "alternatives" in result:
                for alternative in result["alternatives"]:
                    if "words" in alternative:
                        for word_info in alternative["words"]:
                            word_timestamps.append(
                                {
                                    "word": word_info.get("word"),
                                    "start_time": word_info.get("start_time"),
                                    "end_time": word_info.get("end_time"),
                                }
                            )
    return word_timestamps

