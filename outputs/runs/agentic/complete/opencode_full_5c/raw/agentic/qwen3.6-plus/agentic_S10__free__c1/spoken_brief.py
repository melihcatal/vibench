from model_client import create_openai_client, load_config, resolve_model
from model_models import (
    SpokenBriefRequest,
    SpokenBriefResponse,
    build_system_message,
    build_user_message,
)


def generate_spoken_brief(
    text: str,
    style: str = "conversational",
    max_words: int = 150,
    model: str = "gpt-4o-mini",
    temperature: float = 0.5,
) -> SpokenBriefResponse:
    req = SpokenBriefRequest(
        text=text,
        style=style,
        max_words=max_words,
        model=model,
        temperature=temperature,
    )
    config = load_config()
    resolved_model = resolve_model(req.model, config)
    client = create_openai_client()

    style_guidance = {
        "conversational": "Write in a warm, conversational tone as if speaking to a colleague.",
        "formal": "Write in a formal, professional tone suitable for a broadcast.",
        "casual": "Write in a relaxed, casual tone as if chatting with a friend.",
        "technical": "Write in a precise, technical tone for an expert audience.",
        "enthusiastic": "Write in an energetic, enthusiastic tone to engage listeners.",
    }

    tone = style_guidance.get(req.style, style_guidance["conversational"])

    system_prompt = (
        f"You are a broadcast scriptwriter. {tone} "
        f"Condense the provided content into a spoken brief of at most {req.max_words} words. "
        "Use natural spoken-language phrasing. Avoid bullet points, headers, or markdown. "
        "Write as a single flowing paragraph suitable for reading aloud."
    )

    messages = [
        build_system_message(system_prompt),
        build_user_message(req.text),
    ]

    response = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        max_tokens=req.max_words * 2,
        temperature=req.temperature,
    )

    brief = response.choices[0].message.content.strip()
    word_count = len(brief.split())
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return SpokenBriefResponse(
        brief=brief,
        word_count=word_count,
        style=req.style,
        model=response.model,
        usage=usage,
    )


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read() if not sys.stdin.isatty() else ""
    style = sys.argv[1] if len(sys.argv) > 1 else "conversational"
    if input_text:
        result = generate_spoken_brief(input_text, style=style)
        print(result.brief)
