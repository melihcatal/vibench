import asyncio
import aiohttp
from google.cloud import speech_v1p1beta1 as speech
from speech_models import build_config

SUMMARY_TEMPLATE = "Meeting Summary:\n- {points}\n"


def summarize(text: str) -> str:
    # Placeholder: integrate with LLM summarization model (e.g., OpenAI, Cohere)
    # For demo, return first sentence as a stub
    if not text.strip():
        return "No content"
    first_sentence = text.split(".")[0] + "."
    return f"Summary:\n{first_sentence}"


async def meeting_summary(audio_iterable):
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
            full_transcript = ""
            for result in results.get("results", []):
                alt = result.get("alternatives", [{}])[0]
                if not alt.get("is_final"):
                    continue
                full_transcript += alt["transcript"] + " "
            print(summarize(full_transcript))
