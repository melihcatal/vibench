import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODERATION_MODEL = os.environ.get(
    "OPENAI_MODERATION_MODEL", "text-moderation-latest"
)
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL", "gpt-4o")
OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)
OPENAI_TTS_MODEL = os.environ.get("OPENAI_TTS_MODEL", "tts-1")
OPENAI_TTS_VOICE = os.environ.get("OPENAI_TTS_VOICE", "alloy")

_moderation_client = None
_chat_client = None
_embedding_client = None
_tts_client = None


def get_moderation_client():
    global _moderation_client
    if _moderation_client is None:
        _moderation_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    return _moderation_client


def get_chat_client():
    global _chat_client
    if _chat_client is None:
        _chat_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    return _chat_client


def get_embedding_client():
    global _embedding_client
    if _embedding_client is None:
        _embedding_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    return _embedding_client


def get_tts_client():
    global _tts_client
    if _tts_client is None:
        _tts_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    return _tts_client


def call_moderation(text, model=None):
    client = get_moderation_client()
    model = model or OPENAI_MODERATION_MODEL
    response = client.moderations.create(model=model, input=text)
    return response


def call_chat(messages, model=None, temperature=0.0, max_tokens=1024):
    client = get_chat_client()
    model = model or OPENAI_CHAT_MODEL
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response


def call_embedding(texts, model=None):
    client = get_embedding_client()
    model = model or OPENAI_EMBEDDING_MODEL
    if isinstance(texts, str):
        texts = [texts]
    response = client.embeddings.create(model=model, input=texts)
    return response


def call_tts(text, voice=None, model=None, response_format="mp3"):
    client = get_tts_client()
    model = model or OPENAI_TTS_MODEL
    voice = voice or OPENAI_TTS_VOICE
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
    )
    return response
