import asyncio, json


def handle_stream_event(event):
    """Handles partial and final streaming recognition events using DashScope Real-time ASR."""
    if event.get("results"):
        for result in event["results"]:
            if result.get("alternatives"):
                transcript = result["alternatives"][0]["transcript"]
                is_final = result.get("is_final")
                print(f"{'FINAL' if is_final else 'INTERIM'}: {transcript}")


async def listen_for_events():
    from dashscope import SpeechToText

    client = SpeechToText()
    async for event in client.streaming_recognize():
        handle_stream_event(event)


# To run: asyncio.run(listen_for_events())
