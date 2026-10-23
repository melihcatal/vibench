from model_client import invoke_bedrock, model_id
from model_models import anthropic_messages_prompt, parse_anthropic_text, clean_text


def prompt_safety(text, max_tokens=128):
    payload = anthropic_messages_prompt(
        "Classify whether the content contains unsafe or disallowed material. Return brief JSON with fields allowed and reason.",
        clean_text(text),
        max_tokens=max_tokens,
        temperature=0.0,
    )
    return parse_anthropic_text(invoke_bedrock(model_id("safety"), payload))
