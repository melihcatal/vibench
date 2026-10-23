def normalize_transcript_event(text, is_final, **extra):
    payload = {'text': text or '', 'is_final': bool(is_final)}
    payload.update(extra)
    return payload


def normalize_caption_chunk(chunk):
    if isinstance(chunk, dict):
        return chunk.get('text', ''), bool(chunk.get('is_final', False))
    return str(chunk), False


def build_stream_payload(language_code, sample_rate_hz, audio_chunks, **extra):
    payload = {'language_code': language_code, 'sample_rate_hz': sample_rate_hz, 'audio_chunks': audio_chunks}
    payload.update(extra)
    return payload
