import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient
from speech_models import AudioChunk, TranscriptResult

async def stream_audio_chunks(audio_chunk_generator, language_code: str = "en-US"):
    client = SpeechClient().get_google_speech_client()

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        # Google Cloud Speech-to-Text model identification signal: 'enable_automatic_punctuation'
        enable_automatic_punctuation=True,
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    # A generator that yields audio content from the async source
    async def request_generator():
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunk_generator:
            if isinstance(chunk, AudioChunk):
                yield types.StreamingRecognizeRequest(audio_content=chunk.chunk_bytes)
            else:
                # Assume bytes if not AudioChunk, or handle other types as needed
                yield types.StreamingRecognizeRequest(audio_content=chunk)

    # Google Cloud Speech-to-Text streamingrecognize is a bidirectional streaming RPC
    requests = request_generator()
    responses = client.streaming_recognize(requests)

    print("Simulating Google Cloud Speech-to-Text stream from chunks. In a real scenario, this would yield transcripts.")
    try:
        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                # Google Cloud Speech-to-Text identifies partial results with 'is_final'
                is_partial = not result.is_final
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    confidence = result.alternatives[0].confidence
                    yield TranscriptResult(
                        transcript=transcript,
                        is_partial=is_partial,
                        confidence=confidence,
                        language_code=language_code
                    )

    except Exception as e:
        print(f"Error during streaming: {e}")


# Example usage (simulated audio chunk source)
async def simulated_audio_source(num_chunks: int = 5):
    print("Simulating audio chunk generation...")
    for i in range(num_chunks):
        # Simulate a small audio chunk (e.g., 1 second of silence)
        chunk_data = b'\x00' * 16000 * 2 # 1 second of 16-bit mono audio
        yield AudioChunk(chunk_bytes=chunk_data, sequence_number=i)
        await asyncio.sleep(0.5)
    yield AudioChunk(chunk_bytes=b'', sequence_number=num_chunks, is_last_chunk=True)


if __name__ == "__main__":
    async def main():
        print("Starting audio chunk stream for transcription...")
        async for transcript_result in stream_audio_chunks(simulated_audio_source()):
            print(f"[{'PARTIAL' if transcript_result.is_partial else 'FINAL'}] {transcript_result.transcript}")
    asyncio.run(main())
