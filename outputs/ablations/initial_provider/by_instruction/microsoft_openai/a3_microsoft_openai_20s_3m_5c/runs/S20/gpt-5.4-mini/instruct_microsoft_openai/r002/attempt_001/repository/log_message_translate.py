from openai import AzureOpenAI

from observability_client import _client


def log_message_translate(message: str, target_locale: str) -> str:
    client: AzureOpenAI = _client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{"role": "user", "content": f"Translate this log message to {target_locale}:\n{message}"}],
    )
    return response.output_text
