import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client
from speech_models import get_stt_live_options

async def stream_chunks(audio_chunks, model: str = 'nova-2-general'):
    client = get_stt_client()
    options = get_stt_live_options(model=model)
    connection = client.listen.live.v('1').start(options)

    transcript_queue = asyncio.Queue()

    def on_transcript(transcript):
        asyncio.create_task(transcript_queue.put(transcript))

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    async def send_chunks():
        try:
            async for chunk in audio_chunks:
                connection.send(chunk)
        except asyncio.CancelledError:
            pass
        except Exception:
            pass

    send_task = asyncio.create_task(send_chunks())

    try:
        while not send_task.done():
            while True:
                try:
                    transcript = transcript_queue.get_nowait()
                    alternative = transcript.channel.alternatives[0]
                    text = alternative.transcript
                    if text.strip():
                        yield text
                except asyncio.QueueEmpty:
                    break
            await asyncio.sleep(0.01)
    finally:
        send_task.cancel()
        connection.finish()
