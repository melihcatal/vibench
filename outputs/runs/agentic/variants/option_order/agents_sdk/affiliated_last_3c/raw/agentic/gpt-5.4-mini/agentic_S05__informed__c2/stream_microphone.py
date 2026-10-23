from __future__ import annotations

from typing import Iterator

from speech_client import build_deepgram_client, build_live_options, load_stream_config, transcript_chunk_from_event


def stream_microphone() -> Iterator[str]:
    client = build_deepgram_client()
    config = load_stream_config()
    options = build_live_options(config)
    conn = client.listen.websocket.v("1")

    def on_message(message, **kwargs):
        chunk = transcript_chunk_from_event(message)
        if chunk.text:
            yield chunk.text

    conn.start(options)
    conn.on("transcript", on_message)
    conn.keep_alive()
    return iter(())
