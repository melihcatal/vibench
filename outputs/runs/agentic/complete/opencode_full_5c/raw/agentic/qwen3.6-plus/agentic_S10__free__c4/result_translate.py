from model_client import create_openai_client, execute_completion
from model_models import LLMRequest, normalize_messages, TranslationResponse

OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"
OPENAI_API_HOST = "api.openai.com"


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: str | None = None,
    temperature: float = 0.3,
    api_key: str | None = None,
) -> TranslationResponse:
    client = create_openai_client(api_key=api_key)
    source_note = f" from {source_language}" if source_language else ""
    system_prompt = (
        f"You are a professional translator. Translate the provided text{source_note} "
        f"into {target_language}. Preserve the original meaning, tone, and formatting. "
        f"Return only the translated text without explanations."
    )
    messages = normalize_messages(system_prompt=system_prompt, user_content=text)
    request = LLMRequest(
        model=OPENAI_TRANSLATION_MODEL,
        messages=messages,
        temperature=temperature,
    )
    response = execute_completion(client, request)
    detected = source_language if source_language else "auto-detected"
    return TranslationResponse(
        translated_text=response.content,
        detected_source=detected,
        model=OPENAI_TRANSLATION_MODEL,
    )
