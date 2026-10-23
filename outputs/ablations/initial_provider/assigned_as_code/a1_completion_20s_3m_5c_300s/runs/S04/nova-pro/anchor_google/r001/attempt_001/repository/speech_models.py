from google.cloud import speech

def normalize_transcription_response(response):
    transcript = response.results[0].alternatives[0].transcript
    timestamps = [
        {
            "word": word.word,
            "start_time": word.start_time.seconds + word.start_time.nanos * 1e-9,
            "end_time": word.end_time.seconds + word.end_time.nanos * 1e-9,
        }
        for word in response.results[0].alternatives[0].words
    ]
    return {
        "transcript": transcript,
        "timestamps": timestamps,
    }