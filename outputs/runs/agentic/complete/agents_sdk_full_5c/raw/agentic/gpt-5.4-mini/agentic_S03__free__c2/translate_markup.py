from translation_client import create_openai_client, load_config
from translation_models import MarkupTokenizer, normalize_translation_output


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    tokenizer = MarkupTokenizer()
    tokenizer.feed(markup)
    cfg = load_config()
    client = create_openai_client(cfg)
    translated_parts = []
    for segment in tokenizer.segments:
        if segment.kind == "tag":
            translated_parts.append(segment.value)
        else:
            prompt = (
                f"Translate from {source_language} to {target_language}. "
                f"Return only the translated text.\n\nText:\n{segment.value}"
            )
            response = client.responses.create(model=cfg.model, input=prompt)
            translated_parts.append(normalize_translation_output(response.output_text))
    return "".join(translated_parts)
