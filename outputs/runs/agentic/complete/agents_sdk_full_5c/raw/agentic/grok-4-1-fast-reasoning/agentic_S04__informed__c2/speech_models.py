def get_stt_config(diarize: bool = False) -> dict:
    return {
        "speaker_labels": diarize,
        "punctuate": True,
        "format_text": True,
    }
