from model_client import get_openai_client
from model_models import ModelRequest, ModelResponse


def summarize_text(request: ModelRequest) -> ModelResponse:
    client = get_openai_client()

    if not request.prompt:
        raise ValueError("Prompt for summarization cannot be empty.")

    model = request.model if request.model else "gpt-3.5-turbo"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{request.prompt}",
            },
        ],
    )

    summary = response.choices[0].message.content
    return ModelResponse(text=summary, raw_response=response)
