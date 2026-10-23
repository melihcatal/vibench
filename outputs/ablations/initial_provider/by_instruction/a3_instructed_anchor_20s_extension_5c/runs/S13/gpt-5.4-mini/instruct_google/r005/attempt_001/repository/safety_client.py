import os
from typing import Any, Dict, List

from openai import OpenAI

from safety_models import normalize_scores, normalize_text


def get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def moderation_model() -> str:
    return os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def chat_model() -> str:
    return os.environ.get("OPENAI_CHAT_MODEL", "gpt-4.1-mini")


def embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def speech_model() -> str:
    return os.environ.get("OPENAI_SPEECH_MODEL", "gpt-4o-mini-tts")


def moderate_text_payload(text: str) -> Dict[str, Any]:
    client = get_client()
    response = client.moderations.create(model=moderation_model(), input=normalize_text(text))
    result = response.results[0]
    scores = normalize_scores(getattr(result, "category_scores", {}))
    reasons = [name for name, flagged in getattr(result, "categories", {}).items() if flagged]
    return {"allowed": not bool(getattr(result, "flagged", False)), "category_scores": scores, "reasons": reasons, "raw_response": response}


def chat_completion(prompt: str, system: str) -> str:
    client = get_client()
    response = client.chat.completions.create(model=chat_model(), messages=[{"role": "system", "content": system}, {"role": "user", "content": normalize_text(prompt)}])
    return response.choices[0].message.content or ""


def embeddings(texts: List[str]) -> List[List[float]]:
    client = get_client()
    response = client.embeddings.create(model=embedding_model(), input=[normalize_text(t) for t in texts])
    return [item.embedding for item in response.data]


def speech(text: str, voice: str = "alloy") -> bytes:
    client = get_client()
    response = client.audio.speech.create(model=speech_model(), voice=voice, input=normalize_text(text))
    return response.read()
