import openai
import os
from storage_client import get_s3_client


def summarize_stored_asset(bucket: str, key: str) -> str:
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read().decode("utf-8")
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes content.",
            },
            {
                "role": "user",
                "content": f"Please provide a concise summary of the following content:\n\n{content}",
            },
        ],
        max_tokens=200,
    )
    return response.choices[0].message.content
