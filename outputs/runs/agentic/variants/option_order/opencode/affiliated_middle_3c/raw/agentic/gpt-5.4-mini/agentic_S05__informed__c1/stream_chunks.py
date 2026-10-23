from typing import AsyncIterable, AsyncIterator

from speech_client import create_client, live_options, load_config
from speech_models import event_from_result


async def stream_chunks(chunks: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = create_client()
    options = live_options(load_config())
    async with client.listen.asynclive.v("1") as connection:
        await connection.start(options)
        async for chunk in chunks:
            await connection.send(chunk)
            async for result in connection:
                event = event_from_result(result)
                if event.text:
                    yield event.text
                if event.is_final:
                    break
