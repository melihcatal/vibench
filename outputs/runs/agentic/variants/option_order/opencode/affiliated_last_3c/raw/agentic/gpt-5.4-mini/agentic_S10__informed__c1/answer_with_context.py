from openai import OpenAI

from model_client import build_messages, get_model_name, get_openai_client
from model_models import LLMRequest, LLMResponse, normalize_text


def answer_with_context(question: str, context: str) -> LLMResponse:
    req = LLMRequest(
        prompt=normalize_text(question),
        context=normalize_text(context),
        system="Answer the question using only the provided context.",
        model=get_model_name(),
    )
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=req.model,
        messages=build_messages(req.system, req.prompt, req.context),
        temperature=req.temperature,
        max_tokens=req.max_output_tokens,
    )
    return LLMResponse(
        text=response.choices[0].message.content or "",
        model=req.model,
        usage=getattr(response, "usage", None),
    )
