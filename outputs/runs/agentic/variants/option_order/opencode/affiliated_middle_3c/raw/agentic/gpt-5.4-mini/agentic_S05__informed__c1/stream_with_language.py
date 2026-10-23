from speech_client import create_client, live_options, load_config
from speech_models import event_from_result


async def stream_with_language(language: str, punctuation: bool = True):
    client = create_client()
    config = load_config()
    config.language = language
    config.punctuation = punctuation
    async with client.listen.asynclive.v("1") as connection:
        await connection.start(live_options(config))
        async for result in connection:
            event = event_from_result(result)
            if event.text:
                yield event.text
