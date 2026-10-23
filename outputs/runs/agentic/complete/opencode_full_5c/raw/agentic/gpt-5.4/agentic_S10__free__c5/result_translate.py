from model_client import get_chat_model, get_openai_client
from model_models import TextResult, normalize_text


def translate_result(text: str, target_language: str) -> TextResult:
    client = get_openai_client()
    response = client.responses.create(
        model=get_chat_model("translation", default_model="gpt-4.1-mini"),
        input=[
            {
                "role": "system",
                "content": "Translate text accurately while preserving meaning and tone.",
            },
            {
                "role": "user",
                "content": f"Translate the following text to {target_language}:\n\n{text}",
            },
        ],
        max_output_tokens=500,
        temperature=0.1,
    )
    return TextResult(
        provider="OpenAI",
        model=response.model,
        text=normalize_text(response.output_text),
    )
