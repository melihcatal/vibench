from model_client import anthropic_client
from model_models import parse_anthropic_chat


def translate_result(text: str, target_lang: str = "Spanish") -> str:
    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Translate the following text to {target_lang}. Provide only the translation:\n\n{text}",
            }
        ],
    )
    return parse_anthropic_chat(response)
