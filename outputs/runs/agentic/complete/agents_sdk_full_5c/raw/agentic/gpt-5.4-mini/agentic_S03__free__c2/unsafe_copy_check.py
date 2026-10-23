from openai import OpenAI

from translation_client import load_config

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_unsafe_copy(text: str) -> str:
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key) if cfg.api_key else OpenAI()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    return str(response.results[0].categories)
