import os
from functools import lru_cache
from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
DEFAULT_CHAT_MODEL = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4.1-mini')
DEFAULT_TRANSLATION_MODEL = os.getenv('OPENAI_TRANSLATION_MODEL', 'gpt-4.1-mini')
DEFAULT_TTS_MODEL = os.getenv('OPENAI_TTS_MODEL', 'gpt-4o-mini-tts')
DEFAULT_TTS_VOICE = os.getenv('OPENAI_TTS_VOICE', 'alloy')

@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
