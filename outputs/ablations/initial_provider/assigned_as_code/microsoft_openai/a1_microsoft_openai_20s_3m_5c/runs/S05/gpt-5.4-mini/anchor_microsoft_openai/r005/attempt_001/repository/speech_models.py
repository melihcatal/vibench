def normalize_transcript_event(text, is_final, **extra):
    payload = {'text': text or '', 'is_final': bool(is_final)}
    payload.update(extra)
    return payload


def build_stream_request(audio_chunks=None, language_code='en-US', sample_rate_hz=16000, enable_punctuation=True):
    return {
        'audio_chunks': list(audio_chunks or []),
        'language_code': language_code,
        'sample_rate_hz': sample_rate_hz,
        'enable_punctuation': enable_punctuation,
    }
