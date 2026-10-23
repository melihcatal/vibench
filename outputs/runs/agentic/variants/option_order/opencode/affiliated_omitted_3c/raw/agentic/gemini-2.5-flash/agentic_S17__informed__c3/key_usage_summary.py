import os
import anthropic
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse


def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    """Summarizes key usage and crypto events using Anthropic's Claude model."""
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    # Using a recent Claude model, e.g., claude-3-opus-20240229 or claude-3-haiku-20240307
    # Ensure the model selected is appropriate for the task and available via the API.
    model_id = "claude-3-opus-20240229"

    prompt_message = (
        f"Please summarize the following key usage and crypto event data, highlighting any anomalies or critical information:\n\n"
        f"{request.key_usage_data}"
    )

    response = client.messages.create(
        model=model_id,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt_message}],
    )

    summary = response.content[0].text

    return KeyUsageSummaryResponse(summary=summary)
