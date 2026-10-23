import asyncio
import audioop
import speech_recognition as sr

# This example uses Google Cloud Speech-to-Text via the speech_recognition wrapper.
# The provider identifier is the Google Cloud Speech API host.

def stream_microphone(target_sample_rate=16000, chunk_size=1024):
    """Yield raw 16-‑kHz mono audio frames captured from the microphone.

    Args:
        target_sample_rate (int): Desired sample rate for the recognizer.
        chunk_size (int): Number of bytes to read per iteration.

    Yields:
        bytes: raw PCM audio data.
    """
    # Initialize PyAudio
    p = sr.pyaudio.PyAudio()
    stream = p.open(format=sr.pyaudio.paInt16,
                     channels=1,
                     rate=target_sample_rate,
                     input=True,
                     frames_per_buffer=chunk_size,
                     start=False)

    stream.start_stream()
    try:
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            if not data:
                continue
            yield data
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    # Simple test to record 5 seconds and print RMS energy
    async def demo():
        async for audio_chunk in stream_microphone():
            rms = audioop.rms(audio_chunk, 2)  # 2 bytes = int16
            print(f"RMS: {rms}")
            await asyncio.sleep(0)
    asyncio.run(demo())