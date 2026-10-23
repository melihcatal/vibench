from openai import OpenAI

from safety_client import default_chat_model, get_client
from safety_models import TranslationResult


def appeal_translate(text: str, target_language: str = "en") -> TranslationResult:
    client: OpenAI = get_client()
    response = client.responses.create(
        model=default_chat_model(),
        input=[
            {"role": "system", "content": f"Translate the appeal into {target_language} while preserving meaning."},
            {"role": "user", "content": text},
        ],
    )
    return TranslationResult(text=response.output_text)
