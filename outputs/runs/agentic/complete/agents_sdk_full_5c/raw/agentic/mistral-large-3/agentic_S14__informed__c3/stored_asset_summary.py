import os
from storage_client import get_storage_client
from openai import OpenAI

def summarize_stored_asset(bucket_name: str, object_key: str, model: str = "gpt-4o-mini") -> dict:
    """
    Summarizes content extracted from a stored asset using OpenAI GPT.
    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)
    content = blob.download_as_text()

    openai_client = OpenAI(api_key=api_key)
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the following content concisely."},
            {"role": "user", "content": content}
        ]
    )

    return {
        "summary": response.choices[0].message.content,
        "model": model,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }