import os
from elevenlabs.client import ElevenLabs
from typing import List, Dict, Any

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def retrieval_audio_brief(
    retrieved_results: List[Dict[str, Any]], output_file: str
) -> str:
    texts = []
    for result in retrieved_results:
        text = (
            result.get("text") or result.get("snippet", "") or result.get("content", "")
        )
        texts.append(text[:150])
    brief_text = "Audio brief of retrieved search results. " + ". ".join(texts[:5])
    audio = client.generate(
        text=brief_text, voice="Rachel", model="eleven_multilingual_v2"
    )
    with open(output_file, "wb") as f:
        f.write(audio)
    return f"Spoken brief generated and saved to {output_file}"
