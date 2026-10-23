# live_caption_translate.py
import asyncio
import httpx
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client, DEFAULT_LANG

TRANSLATE_TARGET = {
    "en-US": "fr-FR",
    "fr-FR": "en-US",
}

async def translate_live(caption_stream: asyncio.Queue):
    """Streams microphone audio, produces captions, and translates them in real time."""
    client = get_speech_client()
    cfg = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=DEFAULT_LANG,
        enable_automatic_punctuation=True,
    )
    stream_cfg = types.StreamingRecognitionConfig(
        config=cfg,
        interim_results=True,
    )
    
    # Audio generator placeholder (replace with real mic/filereader)
    async def audio_gen():
        for i in range(4):
            yield b"dummy audio chunk"
            await asyncio.sleep(0.5)
    
    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_gen())
    resp_iter = client.streaming_recognize(stream_cfg, requests)
    translator = httpx.AsyncClient(timeout=30.0)
    try:
        api_key = os.getenv("TRANSLATE_API_KEY")
        if not api_key:
            raise RuntimeError("Set TRANSLATE_API_KEY env var")
        endpoint = "https://translation.googleapis.com/language/translate/v2"
        async for resp in resp_iter:
            for result in resp.results:
                if result.is_final:
                    txt = result.alternatives[0].transcript
                    payload = {
                        "q": txt,
                        "source": DEFAULT_LANG.split('-')[0],
                        "target": TRANSLATE_TARGET.get(DEFAULT_LANG, "en-US").split('-')[0],
                        "format": "text",
                        "key": api_key,
                    }
                    r = await translator.post(endpoint, data=payload)
                    data = r.json()
                    translated = data["data"]["translations"][0]["translatedText"]
                    print(f"[Live] {txt} -> {translated}")
    finally:
        await translator.aclose()

if __name__ == "__main__":
    q = asyncio.Queue()
    asyncio.run(translate_live(q))
