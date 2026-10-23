from typing import List

from translation_client import create_openai_client, load_config
from translation_models import normalize_translation_output


def batch_translate(texts: List[str], source_language: str, target_language: str) -> List[str]:
    cfg = load_config()
    client = create_openai_client(cfg)
    results: List[str] = []
    for text in texts:
        prompt = (
            f"Translate from {source_language} to {target_language}. "
            f"Return only the translated text.\n\nText:\n{text}"
        )
        response = client.responses.create(model=cfg.model, input=prompt)
        results.append(normalize_translation_output(response.output_text))
    return results
