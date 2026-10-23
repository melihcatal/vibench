import os
from dataclasses import dataclass

from google import genai


@dataclass
class ModelConfig:
    model: str = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")
    temperature: float = float(os.getenv("GOOGLE_GENAI_TEMPERATURE", "0.2"))
    top_p: float = float(os.getenv("GOOGLE_GENAI_TOP_P", "0.95"))
    max_output_tokens: int = int(os.getenv("GOOGLE_GENAI_MAX_OUTPUT_TOKENS", "1024"))


def get_client() -> genai.Client:
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def get_model_config() -> ModelConfig:
    return ModelConfig()
