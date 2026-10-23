from google import genai

from storage_models import SummaryResult


def stored_asset_summary(text: str, model: str = "gemini-2.0-flash") -> SummaryResult:
    client = genai.Client()
    response = client.models.generate_content(model=model, contents=f"Summarize the following asset text concisely:\n{text}")
    return SummaryResult(text=response.text or "")
