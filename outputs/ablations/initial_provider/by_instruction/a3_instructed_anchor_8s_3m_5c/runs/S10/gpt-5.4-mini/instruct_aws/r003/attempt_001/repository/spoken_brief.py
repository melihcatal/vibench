from model_client import invoke_bedrock, model_id
from model_models import anthropic_messages_prompt, parse_anthropic_text, clean_text


def spoken_brief(text, max_tokens=128):
    payload = anthropic_messages_prompt(
        "Rewrite the content as a short spoken brief suitable for text-to-speech.",
        clean_text(text),
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return parse_anthropic_text(invoke_bedrock(model_id("spoken"), payload))
