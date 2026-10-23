import openai
from storage_client import get_managed_storage_client
from storage_models import HeadObjectResponse

# Use OpenAI's ChatGPT for summarization (managed LLM provider)
openai.api_key = "YOUR_OPENAI_API_KEY"


async def summarize_asset(bucket_name: str, object_key: str) -> str:
    """Extract content from an asset (document, image, video) and produce a concise summary using OpenAI."""
    # Placeholder: assume a helper `extract_content` grabs text/video transcript etc.
    # For demo, we'll just retrieve metadata to show we accessed the object
    storage_client = get_managed_storage_client()
    meta = storage_client.head_object(Bucket=bucket_name, Key=object_key)
    # Example: if metadata indicates PDF, we could OCR it first. Here we just mock.
    dummy_content = "This is a sample asset content that needs summarization."

    summary = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text in two sentences:\n\n{dummy_content}",
            }
        ],
    )["choices"][0]["message"]["content"]
    return summary
