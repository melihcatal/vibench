from model_client import get_openai_client, get_chat_model
from model_models import ChatGenerationRequest, TextResult, normalize_text


def summarize_text(text: str, max_summary_tokens: int = 220) -> TextResult:
    request = ChatGenerationRequest(
        system_prompt="You summarize long documents into concise factual summaries.",
        user_prompt=text,
        max_output_tokens=max_summary_tokens,
        temperature=0.2,
    )
    client = get_openai_client()
    response = client.responses.create(
        model=get_chat_model("summarization", default_model="gpt-4.1-mini"),
        input=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt},
        ],
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
    )
    return TextResult(
        provider="OpenAI",
        model=response.model,
        text=normalize_text(response.output_text),
    )
