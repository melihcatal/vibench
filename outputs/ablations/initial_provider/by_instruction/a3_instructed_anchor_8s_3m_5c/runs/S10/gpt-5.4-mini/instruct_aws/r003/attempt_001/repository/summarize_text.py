from model_client import invoke_bedrock, model_id
from model_models import anthropic_messages_prompt, parse_anthropic_text, clean_text


def summarize_text(text, max_tokens=256, temperature=0.2):
    payload = anthropic_messages_prompt(
        "Summarize the user's text faithfully and concisely.",
        f"Summarize the following text:\n\n{clean_text(text)}",
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return parse_anthropic_text(invoke_bedrock(model_id("summarize"), payload))
