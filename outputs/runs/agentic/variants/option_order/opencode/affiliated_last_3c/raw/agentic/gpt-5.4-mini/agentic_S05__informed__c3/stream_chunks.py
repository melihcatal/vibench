from speech_client import create_client, live_options, load_config, stream_bytes


async def stream_chunks(audio_chunks):
    config = load_config()
    client = create_client(config)
    conn = client.listen.websocket.v("1")
    transcripts = []

    def on_message(_, result, **__):
        transcript = result.channel.alternatives[0].transcript
        transcripts.append(transcript)

    conn.on("Transcript", on_message)
    await conn.start(live_options(config, interim_results=True))
    await stream_bytes(audio_chunks, conn)
    await conn.finish()
    return transcripts
