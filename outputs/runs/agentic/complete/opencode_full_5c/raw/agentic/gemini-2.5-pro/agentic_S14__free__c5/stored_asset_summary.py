from storage_client import get_openai_client
from storage_models import AssetSummary


def summarize_text(text: str, object_name: str) -> AssetSummary:
    """
    Summarizes text using the OpenAI API.

    Args:
        text: The text content to summarize.
        object_name: The name of the source asset object.

    Returns:
        An AssetSummary object.
    """
    openai_client = get_openai_client()

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{text}",
            },
        ],
        temperature=0.3,
        max_tokens=150,
    )

    summary = response.choices[0].message.content.strip()

    return AssetSummary(source_object=object_name, summary=summary)
