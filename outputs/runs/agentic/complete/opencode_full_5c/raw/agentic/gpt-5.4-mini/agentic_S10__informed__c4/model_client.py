import os
from openai import OpenAI

MODEL_FAMILIES = {"summarization": os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"), "structured_extraction": os.getenv("OPENAI_EXTRACT_MODEL", "gpt-4.1-mini"), "qa": os.getenv("OPENAI_QA_MODEL", "gpt-4.1"), "streaming": os.getenv("OPENAI_STREAM_MODEL", "gpt-4.1-mini")}


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def select_chat_model(task_name: str) -> str:
    return MODEL_FAMILIES.get(task_name, os.getenv("OPENAI_DEFAULT_CHAT_MODEL", "gpt-4.1-mini"))
