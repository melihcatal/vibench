import anthropic
import os


def record_summary(document_content: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=100,
        messages=[
            {"role": "user", "content": f"Summarize the following document content: {document_content}"}
        ],
    )
    return response.content[0].text
