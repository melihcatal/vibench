from security_client import SecurityClient
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse


def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    client = SecurityClient()
    prompt = (
        "Summarize the following key usage and crypto events in a concise manner:\n"
    )
    prompt += "\n".join(request.events)

    response = client.gemini_model.generate_content(prompt)
    summary = response.text
    return KeyUsageSummaryResponse(summary=summary)
