from typing import Optional
from model_client import LLMClient
from model_models import LLMRequest, normalize_request, normalize_response


async def answer_with_context(
    question: str,
    context: str,
    system_prompt: Optional[
        str
    ] = "Answer the question using only the provided context. If the answer is not in the context, say 'I don't know'.",
    max_tokens: Optional[int] = None,
) -> str:
    """Answer a question using provided context with Anthropic's hosted LLM."""
    client = LLMClient()
    request = normalize_request(
        {
            "prompt": f"Context: {context}\n\nQuestion: {question}",
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
        }
    )

    response = await client.generate(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
    )
    normalized = normalize_response(response, client.config.model_id)
    return normalized.content
