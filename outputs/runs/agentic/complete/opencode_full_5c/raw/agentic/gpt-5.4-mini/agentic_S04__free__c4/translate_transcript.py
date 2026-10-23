from speech_client import build_client, get_openai_text_model
from speech_models import normalize_text


def translate_transcript(segments, target_language: str = "en"):
    client = build_client()
    text = "\n".join(
        normalize_text(getattr(s, "text", s.get("text") if isinstance(s, dict) else s))
        for s in segments
    )
    response = client.responses.create(
        model=get_openai_text_model(),
        input=f"Translate the transcript to {target_language}:\n{text}",
    )
    return response
