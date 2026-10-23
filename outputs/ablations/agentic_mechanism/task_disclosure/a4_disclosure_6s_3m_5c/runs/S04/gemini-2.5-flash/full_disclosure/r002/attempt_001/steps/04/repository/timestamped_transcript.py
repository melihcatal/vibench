from google.cloud import speech_v1p1beta1 as speech

def get_timestamped_transcript(response):
    """
    Extracts word-level timestamps from a Google Cloud Speech-to-Text transcription response.

    Args:
        response: A google.cloud.speech_v1p1beta1.types.RecognizeResponse object.

    Returns:
        A list of dictionaries, where each dictionary contains the word,
        start time (in seconds), and end time (in seconds).
    """
    timestamped_words = []
    for result in response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                start_time = word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
                end_time = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9
                timestamped_words.append({
                    "word": word_info.word,
                    "start_time": start_time,
                    "end_time": end_time,
                })
    return timestamped_words
