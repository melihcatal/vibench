import asyncio
import os
import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

async def stream_with_language_and_punctuation(deepgram_client: DeepgramClient, language: str = "en-US", punctuate: bool = True):
    """
    Starts a streaming recognizer with specified language and punctuation settings
    using microphone input.
    """
    try:
        RATE = 16000
        CHUNK = 1024
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        dg_connection = deepgram_client.listen.asynclive.v("1")
        print("Successfully connected to Deepgram for language/punctuation stream.")

        def on_transcript(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                print(f"[{'FINAL' if result.is_final else 'PARTIAL'}] Language: {language}, Punctuation: {punctuate} -> {transcript}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

        options = LiveOptions(
            punctuate=punctuate,
            language=language,
            interim_results=True
        )
        await dg_connection.start(options)

        print(f"Starting microphone stream with language='{language}' and punctuate={punctuate}...")
        while True:
            data = stream.read(CHUNK)
            await dg_connection.send(data)

    except Exception as e:
        print(f"Error in stream_with_language_and_punctuation: {e}")
    finally:
        if 'dg_connection' in locals() and dg_connection.is_connecting:
            await dg_connection.finish()
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        if 'audio' in locals():
            audio.terminate()
        print("Language/punctuation stream ended.")

if __name__ == "__main__":
    # This example requires DEEPGRAM_API_KEY environment variable to be set
    # and PyAudio to be installed.
    
    # deepgram_client = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
    # async def main():
    #     # Example 1: English with punctuation
    #     # await stream_with_language_and_punctuation(deepgram_client, language="en-US", punctuate=True)

    #     # Example 2: Spanish without punctuation (for demonstration - needs actual Spanish audio input)
    #     # await stream_with_language_and_punctuation(deepgram_client, language="es", punctuate=False)
    #     pass
    # asyncio.run(main())
    pass
