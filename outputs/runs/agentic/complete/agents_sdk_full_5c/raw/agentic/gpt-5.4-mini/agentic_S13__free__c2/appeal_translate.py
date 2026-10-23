from openai import OpenAI

from safety_client import get_client, load_config
from safety_models import normalize_text


def appeal_translate(appeal_text: str, target_language: str = "English") -> str:
    cfg = load_config()
    client: OpenAI = get_client(cfg)
    response = client.responses.create(
        model=cfg.translate_model,
        input=(
            f"Translate this moderation appeal into {target_language} for reviewer analysis, preserving meaning:\n"
            + normalize_text(appeal_text)
        ),
    )
    return response.output_text if hasattr(response, "output_text") else ""
