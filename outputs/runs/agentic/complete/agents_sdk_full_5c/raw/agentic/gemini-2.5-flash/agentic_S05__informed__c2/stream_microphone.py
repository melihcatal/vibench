import asyncio
import os
import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

async def stream_microphone_audio(deepgram_client: DeepgramClient, language: str = "en-US", punctuation: bool = True):
    """
    Streams microphone audio to Deepgram and yields interim transcripts.
    """
    try:
        # Configuration for PyAudio
        RATE = 16000
        CHUNK = 1024
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        # Connect to Deepgram
        dg_connection = deepgram_client.listen.asynclive.v("1")
        print("Successfully connected to Deepgram.")

        async def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                yield transcript

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            punctuate=punctuation,
            language=language,
            interim_results=True
        )
        await dg_connection.start(options)

        print("Starting microphone stream...")
        while True:
            data = stream.read(CHUNK)
            await dg_connection.send(data)

    except Exception as e:
        print(f"Error in stream_microphone_audio: {e}")
    finally:
        if 'dg_connection' in locals() and dg_connection.is_connecting:
            await dg_connection.finish()
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        if 'audio' in locals():
            audio.terminate()
        print("Microphone stream ended.")

if __name__ == "__main__":
    # This example requires DEEPGRAM_API_KEY environment variable to be set
    # and PyAudio to be installed (pip install pyaudio)
    # On some systems, PyAudio might require portaudio-dev:
    # sudo apt-get install portaudio19-dev
    
    # deepgram_client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
    # async def main():
    #     async for transcript in stream_microphone_audio(deepgram_client):
    #         print(f"Transcript: {transcript}")
    # asyncio.run(main())
    pass
