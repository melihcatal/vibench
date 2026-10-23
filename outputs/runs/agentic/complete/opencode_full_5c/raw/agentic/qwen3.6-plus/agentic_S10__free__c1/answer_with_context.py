from model_client import create_openai_client, load_config, resolve_model
from model_models import (
    AnswerWithContextRequest,
    AnswerWithContextResponse,
    build_system_message,
    build_user_message,
)


def answer_with_context(
    question: str,
    context: str,
    model: str = "gpt-4o",
    max_tokens: int = 512,
    temperature: float = 0.5,
) -> AnswerWithContextResponse:
    req = AnswerWithContextRequest(
        question=question,
        context=context,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    config = load_config()
    resolved_model = resolve_model(req.model, config)
    client = create_openai_client()

    system_prompt = (
        "You are a helpful assistant that answers questions based strictly on the provided context. "
        "If the answer cannot be derived from the context, state that clearly. "
        "Cite the relevant portion of the context when answering."
    )

    user_content = (
        f"<context>\n{req.context}\n</context>\n\n"
        f"<question>\n{req.question}\n</question>"
    )

    messages = [
        build_system_message(system_prompt),
        build_user_message(user_content),
    ]

    response = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
    )

    answer = response.choices[0].message.content.strip()
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return AnswerWithContextResponse(
        answer=answer,
        cited_context=context,
        model=response.model,
        usage=usage,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        q = sys.argv[1]
        ctx = sys.argv[2]
    else:
        q = input("Question: ")
        ctx = input("Context: ")
    result = answer_with_context(q, ctx)
    print(result.answer)
