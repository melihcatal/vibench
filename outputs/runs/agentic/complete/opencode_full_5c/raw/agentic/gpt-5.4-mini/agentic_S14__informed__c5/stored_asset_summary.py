from openai import OpenAI

from storage_models import normalize_text


def stored_asset_summary(text, model="gpt-4.1-mini"):
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=f"Summarize the following asset content concisely:\n{normalize_text(text)}",
    )
    return response.output_text
