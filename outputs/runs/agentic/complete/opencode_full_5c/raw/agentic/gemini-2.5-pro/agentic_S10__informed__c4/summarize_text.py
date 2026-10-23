from model_client import get_client
from model_models import CompletionRequest


def summarize_text(text: str) -> str:
    client = get_client()
    request = CompletionRequest(
        prompt=f"Please summarize the following text:\n\n{text}",
        model="gpt-4o",
    )
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
