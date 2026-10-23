from typing import Iterable, List

from translation_client import get_client
from translation_models import BatchTranslationRequest, TranslationResponse, normalize_text


def batch_translate(texts: Iterable[str], source_language: str, target_language: str, *, model: str = "gpt-4.1-mini") -> List[str]:
    client = get_client()
    items = list(texts)
    request = BatchTranslationRequest(texts=[normalize_text(t) for t in items], source_language=source_language, target_language=target_language, model=model)
    outputs: List[str] = []
    for text in request.texts:
        response = client.responses.create(
            model=request.model,
            input=[
                {"role": "system", "content": "You are a precise translation engine. Return only the translated text."},
                {"role": "user", "content": f"Translate from {request.source_language} to {request.target_language}: {text}"},
            ],
        )
        translated = getattr(response, "output_text", None) or str(response)
        outputs.append(TranslationResponse(text=translated).text)
    return outputs
