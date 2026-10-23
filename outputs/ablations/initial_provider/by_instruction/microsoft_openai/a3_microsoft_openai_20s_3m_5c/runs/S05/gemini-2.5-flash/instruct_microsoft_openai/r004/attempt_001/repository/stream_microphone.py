import asyncio
import collections
from speech_client import SpeechClient
from speech_models import SpeechRecognitionChunk

async def stream_microphone_audio():
    speech_client = SpeechClient()
    # In a real application, this would capture audio from the microphone.
    # For demonstration, we simulate audio chunks.
    print("Simulating microphone audio streaming. Press Ctrl+C to stop.")

    # Simulate a stream of audio chunks
    # In a real scenario, this would be fed by a microphone input library (e.g., pyaudio, sounddevice)
    simulated_audio_chunks = [
        b"This is a simulated audio chunk one.",
        b"And this is another simulated chunk for testing.",
        b"Finally, a third chunk to complete the stream."
    ]

    for i, chunk in enumerate(simulated_audio_chunks):
        # Simulate a small delay for real-time processing
        await asyncio.sleep(1)
        print(f"Processing simulated audio chunk {i+1}...")

        # In a true streaming scenario with OpenAI Whisper, you'd buffer audio
        # and send larger segments or complete utterances. The current example
        # sends each chunk as a separate transcription request, which is not
        # truly streaming in the sense of interim results from a single long audio stream.
        # For this multi-file task, we adhere to the file description.
        try:
            transcript_result = await speech_client.stream_transcribe(chunk)
            yield SpeechRecognitionChunk(text=transcript_result.text, is_final=True) # Simulate final results for each chunk
        except Exception as e:
            print(f"Error during transcription: {e}")
            yield SpeechRecognitionChunk(text="", is_final=False) # Yield empty or error chunk

async def main():
    print("Starting microphone streamer...")
    async for transcript_chunk in stream_microphone_audio():
        print(f"Interim Transcript: {transcript_chunk.text} (Final: {transcript_chunk.is_final})")

if __name__ == "__main__":
    asyncio.run(main())
