from openai import OpenAI

from storage_client import default_summary_model
from storage_models import SummaryResponse


def stored_asset_summary(text: str) -> SummaryResponse:
    client = OpenAI()
    model = default_summary_model()
    response = client.responses.create(model=model, input=f"Summarize the following content:\n{text}")
    summary = response.output_text if hasattr(response, "output_text") else ""
    return SummaryResponse(text=text, summary=summary)
