import os

from elevenlabs.client import ElevenLabs
from openai import OpenAI


def retrieval_audio_brief(results: list[str], language: str = "en") -> bytes:
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI chat completions")
    prompt = "Summarize the retrieved results as a short spoken brief:\n" + "\n".join(f"- {item}" for item in results)
    brief = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    ).choices[0].message.content or ""
    tts = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY", ""))
    if not os.environ.get("ELEVENLABS_API_KEY"):
        raise RuntimeError("ELEVENLABS_API_KEY is required for ElevenLabs TTS")
    audio = tts.text_to_speech.convert(
        text=brief,
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
