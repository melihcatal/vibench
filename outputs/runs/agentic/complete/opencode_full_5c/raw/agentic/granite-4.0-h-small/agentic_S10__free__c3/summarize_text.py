import json
from model_client import ModelClient


def summarize_text(text: str, model_name: str = "gpt-4o-mini") -> str:
    """Summarize the provided long text using the specified hosted LLM.

    Args:
        text (str): The long text to summarize.
        model_name (str): Identifier of the hosted model to use. Defaults to OpenAI GPT-4o-mini.

    Returns:
        str: The generated summary.
    """
    client = ModelClient(model_name)
    # Prompt the model to produce a concise summary.
    prompt = f"Summarize the following text in no more than three sentences:\n\n{text}"
    response = client.complete(prompt)
    return response["text"].strip()
