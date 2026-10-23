from openai import AzureOpenAI

from observability_client import _client


def log_text_safety(message: str) -> str:
    client: AzureOpenAI = _client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{"role": "user", "content": f"Assess if this log text is unsafe, and answer safe or unsafe:\n{message}"}],
    )
    return response.output_text
