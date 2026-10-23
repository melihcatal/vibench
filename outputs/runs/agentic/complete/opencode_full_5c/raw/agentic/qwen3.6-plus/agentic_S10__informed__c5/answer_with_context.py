from model_models import ModelRequest, ModelResponse
from model_client import create_chat_completion


def answer_with_context(
    question: str,
    context: str,
    model: str = "gpt-4o",
    temperature: float = 0.5,
) -> ModelResponse:
    system_prompt = (
        "You are a helpful assistant that answers questions based strictly on the provided context. "
        "If the answer cannot be determined from the context, say so clearly. "
        "Be concise and accurate."
    )

    request = ModelRequest(
        prompt=question,
        context=context,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_tokens=1024,
    )

    return create_chat_completion(request, default_system=system_prompt)


if __name__ == "__main__":
    import sys

    lines = sys.stdin.read().strip().split("\n---\n")
    if len(lines) >= 2:
        ctx = lines[0].strip()
        q = lines[1].strip()
    else:
        ctx = ""
        q = lines[0].strip()
    result = answer_with_context(q, ctx)
    print(result.text)
