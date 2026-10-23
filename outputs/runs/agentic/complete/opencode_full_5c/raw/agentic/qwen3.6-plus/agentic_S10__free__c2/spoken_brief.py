from __future__ import annotations

from typing import Optional

from model_client import call_llm, create_speech
from model_models import LLMRequest, SpokenBriefResponse, normalize_prompt

BRIEF_MODEL = "gpt-4o"
TTS_MODEL = "tts-1"
DEFAULT_VOICE = "alloy"

BRIEF_SYSTEM_PROMPT = (
    "You are a broadcast journalist. Convert the provided text into a concise, "
    "natural-sounding spoken brief suitable for audio delivery. Use short sentences, "
    "clear phrasing, and a conversational tone. Avoid jargon and complex formatting."
)


def generate_spoken_brief(
    text: str,
    max_duration_seconds: int = 60,
    voice: Optional[str] = None,
    tts_model: Optional[str] = None,
    brief_model: Optional[str] = None,
    temperature: float = 0.5,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> SpokenBriefResponse:
    normalized = normalize_prompt(text)
    word_budget = max_duration_seconds * 2
    brief_prompt = (
        f"Create a spoken brief of approximately {word_budget} words or fewer from "
        f"the following content. Write it as if speaking directly to a listener:\n\n"
        f"{normalized}"
    )
    brief_request = LLMRequest(
        model=brief_model or BRIEF_MODEL,
        prompt=brief_prompt,
        system_prompt=BRIEF_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=word_budget * 2,
    )
    brief_response = call_llm(brief_request, api_key=api_key, base_url=base_url)
    spoken_text = brief_response.text
    tts_response = create_speech(
        text=spoken_text,
        voice=voice or DEFAULT_VOICE,
        model=tts_model or TTS_MODEL,
        api_key=api_key,
        base_url=base_url,
    )
    return SpokenBriefResponse(
        text=spoken_text,
        audio_url=tts_response.audio_url,
        model_used=tts_response.model_used,
        voice=tts_response.voice,
        raw=tts_response.raw,
    )


def generate_spoken_brief_text_only(
    text: str,
    max_duration_seconds: int = 60,
    brief_model: Optional[str] = None,
    temperature: float = 0.5,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    normalized = normalize_prompt(text)
    word_budget = max_duration_seconds * 2
    brief_prompt = (
        f"Create a spoken brief of approximately {word_budget} words or fewer from "
        f"the following content. Write it as if speaking directly to a listener:\n\n"
        f"{normalized}"
    )
    brief_request = LLMRequest(
        model=brief_model or BRIEF_MODEL,
        prompt=brief_prompt,
        system_prompt=BRIEF_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=word_budget * 2,
    )
    brief_response = call_llm(brief_request, api_key=api_key, base_url=base_url)
    return brief_response.text


if __name__ == "__main__":
    import os

    response = generate_spoken_brief(
        text="The quarterly earnings report showed a 15 percent increase in revenue...",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(response.text)
