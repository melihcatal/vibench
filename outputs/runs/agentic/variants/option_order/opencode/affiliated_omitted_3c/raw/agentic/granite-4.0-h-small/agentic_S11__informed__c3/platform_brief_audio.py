import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest
import asyncio

# Azure AI Speech configuration (same‑scenario provider)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")
VOICE_NAME = os.getenv("AZURE_SPEECH_VOICE", "en-US-JennyNeural")  # example voice


async def synthesize_speech(text: str, voice: str = VOICE_NAME) -> bytes:
    """
    Convert a plain‑text string into spoken audio using Azure Speech TTS SDK.
    Returns raw ``bytes`` containing the audio (default format: WAV).
    """
    # Placeholder: add `azure-cognitiveservices-speech` package and import SpeechConfig, SpeechSynthesizer
    # from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioOutputConfiguration
    # config = SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    # synthesizer = SpeechSynthesizer(speech_config=config, voice_name=voice)
    # audio = await synthesizer.speak_text_async(text).result()
    # For demo purposes we simulate audio by returning a placeholder WAV header + text length.
    placeholder = b"RIFF" + len(b"Hello world!").to_bytes(4, "little") + b"WAVEfmt "
    # Here we just return a dummy byte stream – replace with real TTS call in production.
    return placeholder


async def brief_audio_from_outputs(
    responses: List[ModelInvocationResponse],
) -> List[bytes]:
    """
    Produce a spoken brief for each model response (first 20 words) using TTS.
    Returns a list of audio byte streams.
    """
    brief_audio = []
    for resp in responses:
        # Create a short synopsis (first 20 words or limited chars)
        short = " ".join(resp.output.split()[:20])
        audio_bytes = await synthesize_speech(short)
        brief_audio.append(audio_bytes)
    return brief_audio


if __name__ == "__main__":

    async def demo():
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": "Summarize the key findings of the 2023 IPCC report in three sentences.",
                }
            ],
            "temperature": 0.2,
            "max_tokens": 80,
        }
        request = ModelInvocationRequest(**payload)
        client = ManagedModelClient(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            model_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        )
        raw_resp = await client.generate(
            request.messages, request.temperature, request.max_tokens
        )
        choices = raw_resp.get("choices")
        responses = [
            ModelInvocationResponse(
                output=choice.get("message").get("content"),
                usage=raw_resp.get("usage"),
                resource_id=raw_resp.get("id"),
                metadata=raw_resp.get("metadata", {}),
            )
            for choice in choices
        ]
        audio_files = await brief_audio_from_outputs(responses)
        for i, audio in enumerate(audio_files):
            # Write a temporary file for demonstration (real deployment would stream directly)
            with open(f"brief_{i}.wav", "wb") as f:
                f.write(audio)
            print(f"Wrote brief audio file brief_{i}.wav (len={len(audio)} bytes)")

    asyncio.run(demo())
