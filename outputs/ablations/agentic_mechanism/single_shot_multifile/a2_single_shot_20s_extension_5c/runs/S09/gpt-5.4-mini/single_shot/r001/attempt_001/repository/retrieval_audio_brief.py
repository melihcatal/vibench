import os
from openai import OpenAI


def retrieval_audio_brief(results: list[dict], voice: str | None = None) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    summary_model = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")
    speech_model = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    brief_prompt = "Summarize these retrieved search results into a concise spoken brief:\n" + "\n".join(
        f"- {item.get('title', '')}: {item.get('snippet', '')}" for item in results
    )
    summary = client.chat.completions.create(
        model=summary_model,
        messages=[{"role": "user", "content": brief_prompt}],
        temperature=0.2,
    ).choices[0].message.content.strip()
    speech = client.audio.speech.create(
        model=speech_model,
        voice=voice or os.getenv("OPENAI_TTS_VOICE", "alloy"),
        input=summary,
    )
    audio_bytes = speech.read() if hasattr(speech, "read") else b""
    return {"summary": summary, "audio_bytes": audio_bytes, "provider": "openai", "model": speech_model}
