def normalize_transcript_response(response):
    results = []
    for result in getattr(response, "results", []):
        alternatives = getattr(result, "alternatives", [])
        transcript = alternatives[0].transcript if alternatives else ""
        words = []
        if alternatives:
            for word in getattr(alternatives[0], "words", []):
                words.append({
                    "word": word.word,
                    "start_time": word.start_time.total_seconds(),
                    "end_time": word.end_time.total_seconds(),
                    "speaker_tag": getattr(word, "speaker_tag", None),
                })
        results.append({
            "transcript": transcript,
            "confidence": alternatives[0].confidence if alternatives else None,
            "words": words,
        })
    return {"results": results}


def build_recognition_config(payload):
    config = {
        "language_code": payload["language_code"],
        "enable_word_time_offsets": payload.get("enable_word_time_offsets", False),
        "enable_automatic_punctuation": payload.get("enable_automatic_punctuation", True),
        "enable_speaker_diarization": payload.get("enable_speaker_diarization", False),
        "diarization_speaker_count": payload.get("diarization_speaker_count"),
    }
    return {key: value for key, value in config.items() if value is not None}
