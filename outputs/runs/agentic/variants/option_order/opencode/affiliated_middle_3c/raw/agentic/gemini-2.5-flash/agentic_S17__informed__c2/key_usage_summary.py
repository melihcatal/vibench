from security_client import security_client
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse


def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    prompt = f"""Summarize the following key usage and crypto events in a concise manner:

{request.logs}

Summary:"""
    response = security_client.gemini_model_llm.generate_content(prompt)
    summary_text = response.text
    return KeyUsageSummaryResponse(summary=summary_text)
