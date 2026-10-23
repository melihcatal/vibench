import asyncio
from dashscope import SpeechRecognizer
from speech_client import get_dashscope_client
from speech_models import TranscriptEvent

async def stream_audio_chunks(audio_source):
    client = get_dashscope_client()
    recognizer = SpeechRecognizer(
        model="paraformer-realtime-v1", 
        format="pcm", 
        sample_rate=16000, 
        callback=handle_result
    )
    
    async for chunk in audio_source:
        recognizer.stream_send(chunk)
        await asyncio.sleep(0)
    recognizer.stream_close()

def handle_result(result):
    event = TranscriptEvent(
        text=result.get("text", ""),
        is_final=result.get("is_final", False),
        timestamp=result.get("timestamp", 0)
    )
    print(f"Chunk Transcript: {event.text} (Final: {event.is_final})")

async def mock_audio_source():
    for i in range(10):
        yield b"mock_audio_chunk"
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(stream_audio_chunks(mock_audio_source()))