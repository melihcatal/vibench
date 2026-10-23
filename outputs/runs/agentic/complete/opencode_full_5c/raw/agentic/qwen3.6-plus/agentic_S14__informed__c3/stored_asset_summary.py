import os
from mistralai import Mistral
from storage_client import get_oss_bucket, normalize_object_key


def summarize_stored_asset(
    bucket_name: str,
    object_key: str,
    model: str = "mistral-large-latest",
    max_tokens: int = 1024,
    temperature: float = 0.3,
) -> dict:
    object_key = normalize_object_key(object_key)
    bucket = get_oss_bucket(bucket_name)

    object_stream = bucket.get_object(object_key)
    document_bytes = object_stream.read()
    content_text = document_bytes.decode("utf-8", errors="replace")

    api_key = os.environ.get("MISTRAL_API_KEY", "")
    client = Mistral(api_key=api_key)

    system_prompt = (
        "You are a document summarization assistant. "
        "Provide a concise, structured summary of the provided content. "
        "Highlight key points, entities, and actionable information."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Summarize the following document content:\n\n{content_text}",
        },
    ]

    chat_response = client.chat.complete(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    summary_text = chat_response.choices[0].message.content

    return {
        "success": True,
        "object_key": object_key,
        "bucket": bucket_name,
        "model": model,
        "summary": summary_text,
        "provider": "Mistral Chat API",
    }
