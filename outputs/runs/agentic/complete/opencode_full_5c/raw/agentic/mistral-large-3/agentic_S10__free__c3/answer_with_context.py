from typing import Optional
from model_client import LLMClient
from model_models import LLMRequest, normalize_response


async def answer_with_context(question: str, context: str) -> str:
    """Answer a question using provided context with Mistral's hosted LLM."""
    client = LLMClient()
    prompt = (
        f"Answer the following question using the provided context. "
        f"If the answer is not in the context, say 'I don't know'.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )
    request = LLMRequest(prompt=prompt, max_tokens=1000)

    response = await client.generate(
        request.prompt, request.temperature, request.max_tokens
    )
    normalized = normalize_response(response)
    await client.close()

    return normalized.choices[0]["message"]["content"]
