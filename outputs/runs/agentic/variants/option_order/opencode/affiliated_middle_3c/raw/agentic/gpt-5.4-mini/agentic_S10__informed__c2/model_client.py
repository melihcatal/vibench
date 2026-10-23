import json
import os
from openai import OpenAI
import deepl
from model_models import normalize_text


def select_chat_model(task: str) -> str:
    mapping = {
        'summarization': os.getenv('OPENAI_CHAT_MODEL', 'gpt-4.1-mini'),
        'extraction': os.getenv('OPENAI_CHAT_MODEL', 'gpt-4.1-mini'),
        'qa': os.getenv('OPENAI_CHAT_MODEL', 'gpt-4.1'),
        'streaming': os.getenv('OPENAI_CHAT_MODEL', 'gpt-4.1-mini'),
    }
    return mapping.get(task, os.getenv('OPENAI_CHAT_MODEL', 'gpt-4.1-mini'))


def get_chat_client() -> OpenAI:
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def chat_messages(instruction: str, content: str):
    return [
        {'role': 'system', 'content': instruction},
        {'role': 'user', 'content': normalize_text(content)},
    ]


def chat_text(response) -> str:
    return response.choices[0].message.content.strip()


def safe_json_loads(text: str):
    return json.loads(text)


def get_translation_client():
    return deepl.Translator(os.getenv('DEEPL_AUTH_KEY', ''))


def select_translation_target(language: str) -> str:
    return language.lower()


def get_embedding_client() -> OpenAI:
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def select_embedding_model() -> str:
    return os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')


def get_tts_client():
    from elevenlabs.client import ElevenLabs
    return ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))


def select_tts_voice() -> str:
    return os.getenv('ELEVENLABS_VOICE', 'Rachel')
