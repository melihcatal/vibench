from model_client import invoke_bedrock, model_id
from model_models import anthropic_messages_prompt, parse_anthropic_text, clean_text


def result_translate(text, target_language, max_tokens=512):
    payload = anthropic_messages_prompt(
        f"Translate the text into {clean_text(target_language)} while preserving meaning.",
        clean_text(text),
        max_tokens=max_tokens,
        temperature=0.1,
    )
    return parse_anthropic_text(invoke_bedrock(model_id("translate"), payload))
