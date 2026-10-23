from openai import OpenAI


def summarize_stored_asset(text: str, model: str = "gpt-4.1-mini"):
    client = OpenAI()
    response = client.responses.create(
        model=model, input=f"Summarize this asset content:\n{text}"
    )
    return response.output_text
