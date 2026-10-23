from model_client import invoke_bedrock, model_id
from model_models import anthropic_messages_prompt, parse_anthropic_text, clean_text


def answer_with_context(question, context, max_tokens=256, temperature=0.2):
    payload = anthropic_messages_prompt(
        "Answer the question using only the provided context when possible.",
        f"Context:\n{clean_text(context)}\n\nQuestion:\n{clean_text(question)}",
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return parse_anthropic_text(invoke_bedrock(model_id("answer"), payload))
