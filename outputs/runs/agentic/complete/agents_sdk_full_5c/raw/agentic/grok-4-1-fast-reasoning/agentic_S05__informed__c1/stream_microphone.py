import asyncio
import pyaudio
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client
from speech_models import get_stt_live_options

async def stream_microphone(
    sample_rate: int = 16000,
    channels: int = 1,
    chunk_size: int = 1024
):
    client = get_stt_client()
    options = get_stt_live_options(language='en-US')
    connection = client.listen.live.v('1').start(options)

    transcript_queue = asyncio.Queue()

    def on_transcript(transcript):
        asyncio.create_task(transcript_queue.put(transcript))

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    p = pyaudio.PyAudio()
    audio_stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size
    )

    try:
        while True:
            audio_chunk = audio_stream.read(chunk_size, exception_on_overflow=False)
            connection.send(audio_chunk)
            while True:
                try:
                    transcript = transcript_queue.get_nowait()
                    alternative = transcript.channel.alternatives[0]
                    text = alternative.transcript
                    if text.strip():
                        yield text
                except asyncio.QueueEmpty:
                    break
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        connection.finish()
