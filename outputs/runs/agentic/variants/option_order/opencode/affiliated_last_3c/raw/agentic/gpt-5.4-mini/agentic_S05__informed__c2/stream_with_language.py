from speech_client import build_deepgram_client, load_speech_config


def start_streaming_recognizer():
    cfg = load_speech_config()
    client = build_deepgram_client()
    return client.transcription.live(
        {
            "language": cfg.language,
            "punctuate": cfg.punctuate,
            "interim_results": cfg.interim_results,
        }
    )
