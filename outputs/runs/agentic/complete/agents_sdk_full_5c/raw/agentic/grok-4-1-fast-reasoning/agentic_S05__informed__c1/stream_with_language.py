import asyncio
from contextlib import asynccontextmanager
from deepgram import LiveOptions
from speech_client import get_stt_client
from speech_models import get_stt_live_options

@asynccontextmanager
async def stream_with_language(
    language: str = 'en-US',
    model: str = 'nova-2-general',
    punctuate: bool = True
):
    client = get_stt_client()
    options = get_stt_live_options(
        language=language,
        model=model,
        punctuate=punctuate
    )
    connection = client.listen.live.v('1').start(options)
    try:
        yield connection
    finally:
        connection.finish()
