from model_client import OpenAIClient
from model_models import LLMRequest, LLMResponse


def summarize_text(text: str, model: str = "gpt-3.5-turbo") -> LLMResponse:
    client = OpenAIClient().get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {"role": "user", "content": f"Summarize the following text: {text}"},
        ],
        max_tokens=LLMRequest.max_tokens,
        temperature=LLMRequest.temperature,
    )
    return LLMResponse(
        generated_text=response.choices[0].message.content,
        finish_reason=response.choices[0].finish_reason,
    )
