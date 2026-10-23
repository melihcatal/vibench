from __future__ import annotations

from openai import OpenAI

from speech_client import OPENAI_TRANSLATE_MODEL, get_client, normalize_text
from speech_models import TranslationRequest


def translate_transcript(transcript: str, target_language: str, source_language: str | None = None) -> dict:
    client: OpenAI = get_client()
    request = TranslationRequest(transcript=normalize_text(transcript), target_language=target_language, source_language=source_language)
    prompt = f"Translate the following transcript into {request.target_language}."
    if request.source_language:
        prompt += f" Source language: {request.source_language}."
    response = client.responses.create(
        model=OPENAI_TRANSLATE_MODEL,
        input=[
            {
                "role": "user",
                "content": [{"type": "input_text", "text": f"{prompt}\n\n{request.transcript}"}],
            }
        ],
    )
    return {"translated_text": response.output_text, "raw": response.model_dump()}
