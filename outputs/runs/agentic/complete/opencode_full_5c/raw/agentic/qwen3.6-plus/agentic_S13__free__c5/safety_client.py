import os
from openai import OpenAI


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")


MODERATION_MODEL = "omni-moderation-latest"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"
TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"

SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
    "harassment",
    "harassment/threatening",
    "illicit",
    "illicit/violent",
]


def build_moderation_payload(text):
    return {
        "model": MODERATION_MODEL,
        "input": text,
    }


def build_chat_payload(system_prompt, user_content, model=CHAT_MODEL, temperature=0.0):
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": temperature,
    }


def build_embedding_payload(texts, model=EMBEDDING_MODEL):
    if isinstance(texts, str):
        texts = [texts]
    return {
        "model": model,
        "input": texts,
    }


def build_tts_payload(text, voice=TTS_VOICE, model=TTS_MODEL):
    return {
        "model": model,
        "voice": voice,
        "input": text,
        "response_format": "mp3",
    }
