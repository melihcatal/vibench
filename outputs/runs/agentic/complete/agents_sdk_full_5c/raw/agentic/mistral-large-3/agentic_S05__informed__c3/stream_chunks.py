import asyncio
from speech_client import get_deepgram_client
from partial_results import handle_partial_result

async def stream_chunks(audio_chunk_queue):
    client = get_deepgram_client()
    deepgram_socket = client.listen.live.v("latest")

    def on_message(ws, message):
        handle_partial_result(message)

    deepgram_socket.registerHandler(deepgram_socket.event.CLOSE, lambda _: print("Deepgram connection closed"))
    deepgram_socket.registerHandler(deepgram_socket.event.MESSAGE, on_message)

    try:
        while True:
            chunk = await audio_chunk_queue.get()
            deepgram_socket.send(chunk)
    except asyncio.CancelledError:
        deepgram_socket.finish()