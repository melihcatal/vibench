from model_client import get_openai_client, resolve_model_name
from model_models import build_chat_messages, extract_usage


def collect_platform_metadata(
    prompt: str, system_prompt: str = None, model: str = None
):
    client = get_openai_client()
    model_name = resolve_model_name(model)
    response = client.chat.completions.create(
        model=model_name, messages=build_chat_messages(prompt, system_prompt)
    )
    output = response.choices[0].message.content
    return {
        "output": output,
        "usage": extract_usage(response),
        "model": model_name,
        "response": response,
    }
