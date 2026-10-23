import asyncio

from speech_client import create_client, live_options, load_config


async def stream_microphone():
    config = load_config()
    client = create_client(config)
    dg_connection = client.listen.websocket.v("1")
    transcripts = []

    def on_message(_, result, **__):
        channel = result.channel
        alternative = channel.alternatives[0]
        transcripts.append((alternative.transcript, channel.is_final))

    dg_connection.on("Transcript", on_message)
    await dg_connection.start(live_options(config, interim_results=True))
    await asyncio.sleep(0)
    return transcripts
