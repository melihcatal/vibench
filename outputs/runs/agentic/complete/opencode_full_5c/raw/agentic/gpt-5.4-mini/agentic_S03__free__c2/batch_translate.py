from translation_client import get_client, get_model_name
from translation_models import TranslationResponse, normalize_text


def batch_translate(
    texts: list[str], source_language: str, target_language: str
) -> list[TranslationResponse]:
    client = get_client()
    model = get_model_name()
    responses: list[TranslationResponse] = []
    for text in texts:
        prompt = f"Translate from {normalize_text(source_language)} to {normalize_text(target_language)}: {normalize_text(text)}"
        result = client.responses.create(model=model, input=prompt)
        responses.append(
            TranslationResponse(translated_text=result.output_text, provider="openai")
        )
    return responses
