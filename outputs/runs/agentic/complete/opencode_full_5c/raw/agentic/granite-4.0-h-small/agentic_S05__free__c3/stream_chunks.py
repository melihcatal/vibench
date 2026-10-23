import asyncio
import aiohttp
from google.cloud import speech_v1p1beta1 as speech

BASE_URL = "https://speech.googleapis.com/v1p1beta1/speech:recognizeStreaming"

client = speech.SpeechClient()  # concrete GCP provider


async def stream_chunks(audio_generator):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True,
        sample_rate_hertz=16000,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    requests = [speech.StreamingRecognizeRequest(streaming_config=streaming_config)]
    # Append audio chunks from async generator
    async for audio_chunk in audio_generator:
        requests.append(speech.StreamingRecognizeRequest(audio_content=audio_chunk))
    payload = {"config": config, "requests": requests}
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL, json=payload) as resp:
            resp.raise_for_status()
            response_data = await resp.json()
            for result in response_data.get("results", []):
                alt = result["alternatives"][0]
                print(f"Partial: {alt['transcript']} (final={result.get('is_final')})")
