import os
from typing import Dict
from openai import OpenAI
from storage_client import get_b2_client, get_bucket_name


def summarize_stored_asset(object_name: str, mime_type: str) -> Dict:
    b2_api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    # Download the file from B2
    downloaded_file = bucket.download_file_by_name(object_name)
    content = downloaded_file.download()

    # Extract text based on MIME type
    text_content = ""
    if mime_type.startswith("text/"):
        text_content = content.decode('utf-8')
    else:
        # For non-text files, use a placeholder or OCR result (not implemented here)
        text_content = "[Binary or unsupported file type]"

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Summarize using OpenAI GPT-4 (model: "gpt-4")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes content."},
            {"role": "user", "content": f"Summarize the following content:\n\n{text_content}"}
        ],
        max_tokens=150
    )

    return {
        "summary": response.choices[0].message.content.strip()
    }