def normalize_chunk(chunk):
    if isinstance(chunk, bytes):
        return chunk
    if isinstance(chunk, memoryview):
        return chunk.tobytes()
    if isinstance(chunk, bytearray):
        return bytes(chunk)
    raise TypeError("audio chunk must be bytes-like")


def normalize_event(text, is_final):
    return {"text": text or "", "is_final": bool(is_final)}


def normalize_payload(payload):
    payload = dict(payload)
    if "audio_chunks" in payload:
        payload["audio_chunks"] = [normalize_chunk(chunk) for chunk in payload["audio_chunks"]]
    return payload
