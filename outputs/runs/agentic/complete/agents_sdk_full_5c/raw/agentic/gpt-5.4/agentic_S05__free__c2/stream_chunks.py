from __future__ import annotations

from collections.abc import AsyncIterable

from deepgram.clients.listen.v1.websocket.async_client import AsyncListenWebSocketClient

from speech_models import AudioChunk


async def stream_audio_chunks(
    connection: AsyncListenWebSocketClient,
    chunks: AsyncIterable[bytes | AudioChunk],
) -> None:
    async for chunk in chunks:
        data = chunk.data if isinstance(chunk, AudioChunk) else chunk
        if data:
            await connection.send(data)
    await connection.finish()
