import os
from openai import OpenAI, AsyncOpenAI


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODERATION_MODEL = "text-moderation-latest"
OPENAI_CHAT_MODEL = "gpt-4o"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_TTS_MODEL = "tts-1"
OPENAI_TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def get_api_key():
    return os.environ.get("OPENAI_API_KEY")


def get_openai_client(timeout=30.0):
    api_key = get_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(
        api_key=api_key,
        base_url=OPENAI_API_BASE,
        timeout=timeout,
    )


def get_async_openai_client(timeout=30.0):
    api_key = get_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return AsyncOpenAI(
        api_key=api_key,
        base_url=OPENAI_API_BASE,
        timeout=timeout,
    )


def get_moderation_categories():
    return [
        "sexual",
        "hate",
        "harassment",
        "self-harm",
        "sexual/minors",
        "hate/threatening",
        "violence/graphic",
        "self-harm/intent",
        "self-harm/instructions",
        "harassment/threatening",
        "violence",
    ]


def build_moderation_payload(text):
    return {"input": text, "model": OPENAI_MODERATION_MODEL}


def build_chat_payload(messages, temperature=0.0, max_tokens=512):
    return {
        "model": OPENAI_CHAT_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }


def build_embedding_payload(texts):
    if isinstance(texts, str):
        texts = [texts]
    return {
        "model": OPENAI_EMBEDDING_MODEL,
        "input": texts,
        "encoding_format": "float",
    }


def build_tts_payload(text, voice="alloy", response_format="mp3"):
    return {
        "model": OPENAI_TTS_MODEL,
        "input": text,
        "voice": voice,
        "response_format": response_format,
    }


def validate_text_input(text):
    if not isinstance(text, str):
        raise TypeError("Text input must be a string")
    if not text.strip():
        raise ValueError("Text input cannot be empty")
    if len(text) > 32768:
        raise ValueError("Text input exceeds maximum length of 32768 characters")
    return text.strip()


def validate_batch_input(texts):
    if not isinstance(texts, list):
        raise TypeError("Batch input must be a list of strings")
    if len(texts) == 0:
        raise ValueError("Batch input cannot be empty")
    if len(texts) > 100:
        raise ValueError("Batch input exceeds maximum of 100 items")
    return [validate_text_input(t) for t in texts]
