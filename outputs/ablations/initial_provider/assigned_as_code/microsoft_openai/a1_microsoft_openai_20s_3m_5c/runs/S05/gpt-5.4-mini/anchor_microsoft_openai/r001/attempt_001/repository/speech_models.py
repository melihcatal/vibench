def make_stream_payload(audio_chunks, language_code='en-US', sample_rate_hz=16000):
    return {'audio_chunks': audio_chunks, 'language_code': language_code, 'sample_rate_hz': sample_rate_hz}


def normalize_event(text, is_final):
    return {'text': (text or '').strip(), 'is_final': bool(is_final)}


def build_language_payload(audio_chunks, language_code, sample_rate_hz, enable_punctuation):
    return {'audio_chunks': audio_chunks, 'language_code': language_code, 'sample_rate_hz': sample_rate_hz, 'enable_punctuation': enable_punctuation}
