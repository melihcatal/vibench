import os
from openai import OpenAI
from assemblyai import AssemblyAI
from deepgram import DeepgramClient


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


def get_assemblyai_client() -> AssemblyAI:
    return AssemblyAI(api_key=ASSEMBLYAI_API_KEY)


def get_deepgram_client() -> DeepgramClient:
    return DeepgramClient(DEEPGRAM_API_KEY)


def validate_openai_key() -> bool:
    return bool(OPENAI_API_KEY)


def validate_assemblyai_key() -> bool:
    return bool(ASSEMBLYAI_API_KEY)


def validate_deepgram_key() -> bool:
    return bool(DEEPGRAM_API_KEY)


def get_openai_base_url() -> str:
    return "https://api.openai.com/v1"


def get_assemblyai_base_url() -> str:
    return "https://api.assemblyai.com/v2"


def get_deepgram_base_url() -> str:
    return "https://api.deepgram.com/v1"


OPENAI_WHISPER_MODEL = "whisper-1"
OPENAI_SUMMARY_MODEL = "gpt-4o"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
ASSEMBLYAI_TRANSCRIBE_MODEL = "assemblyai_default"
DEEPGRAM_NOVA_MODEL = "nova-3"
