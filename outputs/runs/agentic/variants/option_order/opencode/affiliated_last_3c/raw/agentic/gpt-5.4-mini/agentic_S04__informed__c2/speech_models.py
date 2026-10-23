def normalize_transcript_payload(payload):
    if isinstance(payload, dict):
        return {
            "id": payload.get("id"),
            "status": payload.get("status"),
            "text": payload.get("text", ""),
            "language_code": payload.get("language_code"),
            "words": payload.get("words", []),
            "utterances": payload.get("utterances", []),
            "chapters": payload.get("chapters", []),
        }
    return {
        "id": None,
        "status": None,
        "text": "",
        "language_code": None,
        "words": [],
        "utterances": [],
        "chapters": [],
    }


def build_transcription_request(audio_url, **kwargs):
    payload = {"audio_url": audio_url}
    payload.update(kwargs)
    return payload


def build_diarization_request(audio_url, speaker_labels=True, **kwargs):
    payload = {"audio_url": audio_url, "speaker_labels": speaker_labels}
    payload.update(kwargs)
    return payload


def build_timestamped_request(audio_url, punctuate=True, format_text=True, **kwargs):
    payload = {
        "audio_url": audio_url,
        "punctuate": punctuate,
        "format_text": format_text,
    }
    payload.update(kwargs)
    return payload
