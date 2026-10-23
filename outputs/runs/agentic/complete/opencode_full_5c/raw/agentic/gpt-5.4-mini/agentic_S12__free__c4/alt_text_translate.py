from openai import OpenAI

from vision_client import load_config, get_openai_client


def alt_text_translate(text, target_language):
    cfg = load_config()
    client: OpenAI = get_openai_client(cfg)
    response = client.responses.create(
        model=cfg.translation_model,
        input=f"Translate this image description into {target_language}: {text}",
    )
    return response.output_text.strip()
