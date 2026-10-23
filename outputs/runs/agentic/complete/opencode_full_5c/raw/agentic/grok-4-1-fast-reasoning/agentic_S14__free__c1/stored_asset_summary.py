import openai
import os
from storage_client import get_storage_client


def summarize_stored_asset(bucket: str, object_key: str) -> str:
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    s3_client = get_storage_client()
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    content = response["Body"].read().decode("utf-8", errors="ignore")
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following content concisely:\n\n{content[:10000]}",
            }
        ],
        max_tokens=300,
    )
    return completion.choices[0].message.content
