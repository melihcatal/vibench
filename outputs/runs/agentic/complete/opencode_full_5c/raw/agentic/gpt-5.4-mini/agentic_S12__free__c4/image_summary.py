from openai import OpenAI

from vision_client import load_config, get_openai_client


def image_summary(labels, description, text):
    cfg = load_config()
    client: OpenAI = get_openai_client(cfg)
    prompt = f"Summarize the visual analysis in a concise paragraph. Labels: {labels}. Description: {description}. Text: {text}."
    response = client.responses.create(
        model=cfg.translation_model,
        input=prompt,
    )
    return response.output_text.strip()
