from openai import AzureOpenAI

from observability_client import _client


def incident_summary(error_findings: str) -> str:
    client: AzureOpenAI = _client()
    response = client.responses.create(
        model="gpt-4.1",
        input=[{"role": "user", "content": f"Summarize for incident review:\n{error_findings}"}],
    )
    return response.output_text
