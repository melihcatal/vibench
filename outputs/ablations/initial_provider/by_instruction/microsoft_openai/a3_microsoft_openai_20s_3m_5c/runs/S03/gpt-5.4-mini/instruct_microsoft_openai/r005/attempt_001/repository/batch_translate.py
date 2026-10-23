from translation_client import get_config, get_openai_client, get_azure_translation_client, normalize_language
from translation_models import TranslationResponse, normalize_text


def batch_translate(texts: list[str], source_language: str, target_language: str) -> list[TranslationResponse]:
    cfg = get_config()
    src = normalize_language(source_language)
    tgt = normalize_language(target_language)
    if cfg.provider == "azure":
        client = get_azure_translation_client()
        results = client.translate(content=[normalize_text(t) for t in texts], to=[tgt], from_parameter=src)
        return [TranslationResponse(translated_text=item.translations[0].text if item.translations else "", provider="azure") for item in results]
    client = get_openai_client()
    responses: list[TranslationResponse] = []
    for text in texts:
        result = client.responses.create(model=cfg.openai_model, input=f"Translate from {src} to {tgt}: {normalize_text(text)}")
        responses.append(TranslationResponse(translated_text=result.output_text if hasattr(result, "output_text") else "", provider="openai"))
    return responses
