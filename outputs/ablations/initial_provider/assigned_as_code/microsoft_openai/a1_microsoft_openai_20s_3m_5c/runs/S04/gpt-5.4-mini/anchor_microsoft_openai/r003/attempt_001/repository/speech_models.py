def normalize_payload(payload):
    return {
        "language_code": payload["language_code"],
        "audio_uri": payload["audio_uri"],
    }


def normalize_transcript_response(data):
    return {
        "job_id": data.get("self") or data.get("id"),
        "status": data.get("status"),
        "transcript": data.get("combinedRecognizedPhrases") or data.get("displayText") or data.get("transcript"),
    }
