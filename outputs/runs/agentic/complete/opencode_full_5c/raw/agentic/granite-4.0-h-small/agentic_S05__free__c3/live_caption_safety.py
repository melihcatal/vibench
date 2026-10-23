import re
import asyncio
import aiohttp
from google.cloud import dlp_v2 as dlp
from speech_models import build_config


def unsafe_pattern() -> re.Pattern:
    # Simple example: profanity words list – replace with real list or external service
    words = ["badword1", "badword2", "expletive"]
    return re.compile(
        r"\\b(" + "|\\b".join(map(re.escape, words)) + r")\\b", re.IGNORECASE
    )


def filter_unsafe(text: str) -> bool:
    return not unsafe_pattern().search(text)


def safe_check(text: str) -> str:
    # Placeholder for a real DLP API call to Google Cloud DLP
    if filter_unsafe(text):
        return text
    else:
        return "[CONTENT_REMOVED]"


async def live_caption_safety(audio_iterable):
    client = speech.SpeechClient()  # concrete GCP provider
    config = build_config(language_code="en-US")
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=False
    )
    requests = [speech.StreamingRecognizeRequest(streaming_config=streaming_config)]
    async for chunk in audio_iterable:
        requests.append(speech.StreamingRecognizeRequest(audio_content=chunk))
    payload = {"config": config, "requests": requests}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://speech.googleapis.com/v1p1beta1/speech:recognizeStreaming",
            json=payload,
        ) as resp:
            results = await resp.json()
            for result in results.get("results", []):
                alt = result.get("alternatives", [{}])[0]
                if not alt.get("is_final"):
                    continue
                caption = alt["transcript"]
                safe_caption = safe_check(caption)
                print(f"Safe caption: {safe_caption}")
