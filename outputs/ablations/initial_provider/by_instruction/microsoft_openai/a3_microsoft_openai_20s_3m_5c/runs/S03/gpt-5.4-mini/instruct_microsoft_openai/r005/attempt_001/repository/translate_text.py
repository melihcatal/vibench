from translation_client import get_config, get_openai_client, get_azure_translation_client, normalize_language
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_language: str, target_language: str) -> TranslationResponse:
    cfg = get_config()
    req = TranslationRequest(normalize_text(text), normalize_language(source_language), normalize_language(target_language))
    if cfg.provider == "azure":
        client = get_azure_translation_client()
        result = client.translate(content=[req.text], to=[req.target_language], from_parameter=req.source_language)
        translated = result[0].translations[0].text if result and result[0].translations else ""
        return TranslationResponse(translated_text=translated, provider="azure")
    client = get_openai_client()
    response = client.responses.create(
        model=cfg.openai_model,
        input=f"Translate from {req.source_language} to {req.target_language}: {req.text}",
    )
    translated = response.output_text if hasattr(response, "output_text") else ""
    return TranslationResponse(translated_text=translated, provider="openai")
