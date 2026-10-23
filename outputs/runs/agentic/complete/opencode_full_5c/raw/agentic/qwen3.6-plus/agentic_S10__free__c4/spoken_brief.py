import io
from model_client import create_openai_client, execute_completion
from model_models import (
    LLMRequest,
    normalize_messages,
    SpokenBriefRequest,
    SpokenBriefResponse,
)

OPENAI_BRIEF_MODEL = "gpt-4o-mini"
OPENAI_TTS_MODEL = "tts-1"
OPENAI_API_HOST = "api.openai.com"


def generate_spoken_brief(
    text: str,
    target_length_seconds: int = 30,
    voice: str = "alloy",
    api_key: str | None = None,
) -> SpokenBriefResponse:
    client = create_openai_client(api_key=api_key)
    words_per_minute = 150
    target_words = int(target_length_seconds / 60 * words_per_minute)
    system_prompt = (
        "You are a broadcast assistant. Condense the provided text into a natural, "
        "conversational spoken brief suitable for audio delivery. "
        f"Keep it to approximately {target_words} words. "
        "Use clear, spoken-friendly language with short sentences. "
        "Avoid markdown, lists, or formatting that does not translate well to speech."
    )
    messages = normalize_messages(system_prompt=system_prompt, user_content=text)
    request = LLMRequest(
        model=OPENAI_BRIEF_MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=target_words * 2,
    )
    llm_response = execute_completion(client, request)
    brief_text = llm_response.content
    tts_response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=voice,
        input=brief_text,
        response_format="mp3",
    )
    audio_buffer = io.BytesIO()
    for chunk in tts_response.iter_bytes():
        audio_buffer.write(chunk)
    audio_buffer.seek(0)
    return SpokenBriefResponse(
        audio_data=audio_buffer.read(),
        brief_text=brief_text,
        audio_format="mp3",
    )
