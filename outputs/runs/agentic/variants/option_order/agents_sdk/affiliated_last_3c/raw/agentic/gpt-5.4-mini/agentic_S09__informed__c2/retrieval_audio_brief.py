import os
from typing import Iterable

from elevenlabs import generate, save


def retrieval_audio_brief(results: Iterable[str], output_path: str = "retrieval_brief.mp3") -> str:
    prompt = "Briefly summarize these retrieved results: " + " | ".join(results)
    audio = generate(text=prompt, voice=os.getenv("ELEVENLABS_VOICE", "Rachel"), model="eleven_multilingual_v2")
    save(audio, output_path)
    return output_path
