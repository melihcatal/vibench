from google.cloud.speech_v1 import enums

def normalize_transcript(transcript):
    return transcript.lower()

def extract_word_timestamps(response):
    word_timestamps = []
    for result in response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                word_timestamps.append((word_info.word, word_info.start_time, word_info.end_time))
    return word_timestamps