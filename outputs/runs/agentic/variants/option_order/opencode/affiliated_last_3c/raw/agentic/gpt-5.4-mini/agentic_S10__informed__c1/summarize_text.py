from openai import OpenAI

from model_client import build_messages, get_model_name, get_openai_client
from model_models import LLMRequest, LLMResponse, normalize_text


def summarize_text(text: str, max_output_tokens: int = 256) -> LLMResponse:
    req = LLMRequest(
        prompt=normalize_text(text),
        system="Summarize the provided text concisely.",
        max_output_tokens=max_output_tokens,
        model=get_model_name(),
    )
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=req.model,
        messages=build_messages(req.system, req.prompt),
        temperature=req.temperature,
        max_tokens=req.max_output_tokens,
    )
    return LLMResponse(
        text=response.choices[0].message.content or "",
        model=req.model,
        usage=getattr(response, "usage", None),
    )
