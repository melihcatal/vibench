import os

from openai import OpenAI


def archive_image_analysis(bucket_name: str, artifact_name: str, content: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": f"Prepare this analysis artifact for archive in managed object storage bucket {bucket_name} with key {artifact_name}: {content}",
            }
        ],
        max_output_tokens=120,
    )
    return getattr(response, "output_text", "") or ""
