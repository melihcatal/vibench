import google.generativeai as genai
from security_client import get_gemini_model
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse
import os


def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    model = get_gemini_model()
    prompt = f"Summarize the following key usage and crypto events:\n\n{request.usage_logs}\n\nSummary:"
    response = model.generate_content(prompt)
    return KeyUsageSummaryResponse(summary=response.text)
