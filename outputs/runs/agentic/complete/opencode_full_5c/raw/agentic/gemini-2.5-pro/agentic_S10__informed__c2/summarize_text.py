from model_client import get_openai_client
from model_models import Prompt, Response


def summarize(prompt: Prompt) -> Response:
    client = get_openai_client()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {"role": "user", "content": prompt.text},
        ],
    )
    summary = completion.choices[0].message.content
    return Response(text=summary)
