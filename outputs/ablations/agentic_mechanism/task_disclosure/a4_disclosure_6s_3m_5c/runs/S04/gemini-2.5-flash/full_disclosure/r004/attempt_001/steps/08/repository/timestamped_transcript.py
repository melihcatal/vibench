from google.cloud import speech_v1p1beta1 as speech

def get_word_timestamps(transcription_result):
    """
    Extracts word-level timestamps from a Google Cloud Speech-to-Text transcription result.

    Args:
        transcription_result (dict): The JSON response from Google Cloud Speech-to-Text API.

    Returns:
        list: A list of dictionaries, where each dictionary contains 'word',
              'start_time' (in seconds), and 'end_time' (in seconds).
    """
    timestamps = []
    if "results" in transcription_result:
        for result in transcription_result["results"]:
            if "alternatives" in result:
                for alternative in result["alternatives"]:
                    if "words" in alternative:
                        for word_info in alternative["words"]:
                            start_seconds = int(word_info["startTime"][:-1]) if "startTime" in word_info and word_info["startTime"] else 0
                            end_seconds = int(word_info["endTime"][:-1]) if "endTime" in word_info and word_info["endTime"] else 0
                            timestamps.append({
                                "word": word_info.get("word"),
                                "start_time": start_seconds,
                                "end_time": end_seconds,
                            })
    return timestamps
