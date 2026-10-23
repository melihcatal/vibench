from openai import OpenAI

from vision_client import load_config, get_openai_client


def visual_safety_text(labels):
    cfg = load_config()
    client: OpenAI = get_openai_client(cfg)
    response = client.responses.create(
        model=cfg.translation_model,
        input=f"Check these visual labels for unsafe or policy-sensitive text and return a concise risk note: {labels}",
    )
    return response.output_text.strip()
