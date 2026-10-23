import os

from openai import OpenAI


def stored_asset_summary(text: str, model: str = "gpt-5.4-mini") -> str:
    client = OpenAI()
    response = client.responses.create(
        model=model, input=f"Summarize this asset content concisely:\n{text}"
    )
    return response.output_text


if __name__ == "__main__":
    print(stored_asset_summary(os.environ["TEXT"]))
