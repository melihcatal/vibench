import os
import openai
from storage_client import get_s3_client

def summarize_asset(bucket_name: str, object_key: str) -> str:
    """Summarize the content of a stored asset (e.g., a PDF or text file) using GPT-4o.

    This uses OpenAI's Chat Completion endpoint. Credentials come from OPENAI_API_KEY.
    The asset is first fetched, then a concise summary is requested.
    """
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    content = obj['Body'].read().decode('utf-8')

    # Simple zero-shot summarization prompt
    prompt = (
        "You are a helpful assistant. Summarize the following document in 2-3 sentences, preserving key points.\\n\\n{}"
    ).format(content)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return response.choices[0].message.content.strip()
