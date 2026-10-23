# Summarize meeting transcript live using OpenAI ChatGPT.
import asyncio
import httpx
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY env var")

async def summarize_meeting(caption_stream: asyncio.Queue):
    """Live summarization of meeting captions."""
    client = get_speech_client()
    cfg = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    stream_cfg = types.StreamingRecognitionConfig(
        config=cfg,
        interim_results=True,
    )
    
    # Placeholder audio generator
    async def audio_gen():
        for i in range(5):
            yield b"dummy audio chunk"
            await asyncio.sleep(0.4)
    
    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_gen())
    resp_iter = client.streaming_recognize(stream_cfg, requests)
    client = httpx.AsyncClient(timeout=30.0)
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        buffer: list[str] = []
        async for resp in resp_iter:
            for result in resp.results:
                if result.is_final:
                    text = result.alternatives[0].transcript
                    buffer.append(text)
                    if len(' '.join(buffer)) > 2000:
                        await send_to_llm(buffer, client)
                        buffer.clear()
        if buffer:
            await send_to_llm(buffer, client)
    finally:
        await client.aclose()

async def send_to_llm(text_parts, client):
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Summarize the following meeting transcript in two concise sentences:\n\n" + ' '.join(text_parts)}],
        "temperature": 0.2,
    }
    r = await client.post(url, json=payload, headers=headers)
    summary = r.json()["choices"][0]["message"]["content"]
    print("[SUMMARY]", summary)

if __name__ == "__main__":
    q = asyncio.Queue()
    asyncio.run(summarize_meeting(q))
