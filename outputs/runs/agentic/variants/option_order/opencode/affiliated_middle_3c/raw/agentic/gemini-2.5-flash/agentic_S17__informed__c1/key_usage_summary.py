import os
import google.generativeai as genai
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse

def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text generation

    prompt = f"Summarize the following key usage and cryptographic event logs:
\n{request.audit_logs}\n\nProvide a concise summary highlighting important events, potential anomalies, and overall usage patterns."

    try:
        response = model.generate_content(prompt)
        return KeyUsageSummaryResponse(summary=response.text)
    except Exception as e:
        raise RuntimeError(f"Failed to summarize key usage with Google Gemini API: {e}")
