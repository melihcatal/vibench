from speech_client import create_client, live_options, load_config


async def stream_with_language(language: str, audio_chunks):
    config = load_config(language=language, punctuate=True)
    client = create_client(config)
    conn = client.listen.websocket.v("1")
    transcript = []

    def on_message(_, result, **__):
        transcript.append(result.channel.alternatives[0].transcript)

    conn.on("Transcript", on_message)
    await conn.start(live_options(config, interim_results=True))
    for chunk in audio_chunks:
        if chunk:
            await conn.send(chunk)
    await conn.finish()
    return transcript
