from translation_client import get_config, get_openai_client
from translation_models import normalize_mapping


def translate_dictionary_values(data: dict, source_language: str, target_language: str) -> dict:
    cfg = get_config()
    client = get_openai_client()
    out = {}
    for key, value in normalize_mapping(data).items():
        if isinstance(value, str):
            response = client.responses.create(model=cfg.openai_model, input=f"Translate from {source_language} to {target_language}: {value}")
            out[key] = response.output_text if hasattr(response, "output_text") else value
        else:
            out[key] = value
    return out
