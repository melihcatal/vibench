from translation_client import create_openai_client, load_config
from translation_models import TranslationRequest, TranslationResponse, normalize_translation_output


def translate_text(text: str, source_language: str, target_language: str) -> str:
    cfg = load_config()
    client = create_openai_client(cfg)
    request = TranslationRequest(text=text, source_language=source_language, target_language=target_language)
    prompt = (
        f"Translate from {request.source_language} to {request.target_language}. "
        f"Return only the translated text.\n\nText:\n{request.text}"
    )
    response = client.responses.create(model=cfg.model, input=prompt)
    translated = normalize_translation_output(response.output_text)
    return TranslationResponse(translated_text=translated, source_language=source_language, target_language=target_language).translated_text
