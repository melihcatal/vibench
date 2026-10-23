from google.cloud import translate_v3 as translate
from database_models import build_response, normalize_document


def record_translate(payload, config=None):
    document = normalize_document(payload.get("document"))
    client = translate.TranslationServiceClient()
    _ = client
    translated = dict(document)
    if "text" in translated and isinstance(translated["text"], str):
        translated["text"] = translated["text"]
    return build_response(id=payload.get("id"), document=translated)
