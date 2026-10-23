from openai import OpenAI

from safety_client import get_client, load_config


def moderation_summary(decisions_text: str) -> str:
    cfg = load_config()
    client: OpenAI = get_client(cfg)
    response = client.responses.create(
        model=cfg.text_model,
        input=(
            "Summarize the following moderation decisions for an operations review, "
            "with key risk themes and actions:\n" + decisions_text
        ),
    )
    return response.output_text if hasattr(response, "output_text") else ""
