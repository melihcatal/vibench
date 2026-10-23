def normalize_transcription_response(response):
    return {
        'transcript': response.results[0].alternatives[0].transcript,
        'confidence': response.results[0].alternatives[0].confidence,
    }

def normalize_diarization_response(response):
    return {
        'speaker_labels': [label.speaker_tag for label in response.speaker_labels],
    }

def normalize_timestamped_response(response):
    return {
        'timestamps': [(word.start_time, word.end_time) for word in response.results[0].alternatives[0].words],
    }