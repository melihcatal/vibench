from __future__ import annotations

from typing import Iterator, Optional

from speech_client import build_deepgram_client, build_live_options, load_stream_config, transcript_chunk_from_event


def start_streaming_recognizer(language_code: Optional[str] = None, punctuation: bool = True) -> Iterator[str]:
    client = build_deepgram_client()
    config = load_stream_config()
    if language_code:
        config.language_code = language_code
    config.enable_automatic_punctuation = punctuation
    options = build_live_options(config)
    conn = client.listen.websocket.v("1")
    conn.start(options)

    def on_message(message, **kwargs):
        chunk = transcript_chunk_from_event(message)
        if chunk.text:
            yield chunk.text

    conn.on("transcript", on_message)
    return iter(())
