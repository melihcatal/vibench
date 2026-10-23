import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_deepgram_client

# A mock microphone class to simulate audio streaming
class Microphone:
    def __init__(self, chunk_size=1024):
        self._chunk_size = chunk_size

    async def start(self):
        # In a real scenario, this would initialize the audio stream
        await asyncio.sleep(0.1)

    async def read_chunk(self):
        # In a real scenario, this would read from the microphone
        # Here we simulate it by yielding silent audio chunks
        await asyncio.sleep(0.1)  # Simulate audio capture interval
        return b'\x00' * self._chunk_size

    async def stop(self):
        await asyncio.sleep(0.1)


async def stream_from_microphone():
    """Streams audio from a (simulated) microphone and prints the transcript."""
    deepgram_client = get_deepgram_client()
    
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcript: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = {
            "model": "nova-2",
            "language": "en-US",
            "interim_results": True,
        }
        await dg_connection.start(options)

        mic = Microphone()
        await mic.start()

        # Simulate streaming for a short duration
        for _ in range(20):
            chunk = await mic.read_chunk()
            await dg_connection.send(chunk)
        
        await mic.stop()
        await dg_connection.finish()

    except Exception as e:
        print(f"Error during streaming: {e}")
