import os

from openai import OpenAI

from storage_models import SummaryResult


def stored_asset_summary(source_text: str) -> SummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize the following content concisely: {source_text}",
    )
    return SummaryResult(source_text=source_text, summary=response.output_text, raw={"model": "gpt-5.4-mini"})
