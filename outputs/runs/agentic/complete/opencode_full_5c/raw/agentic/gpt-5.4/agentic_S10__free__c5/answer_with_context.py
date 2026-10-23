from model_client import get_openai_client, get_chat_model
from model_models import AnswerResult, ChatGenerationRequest, normalize_text


def answer_with_context(question: str, context: str) -> AnswerResult:
    request = ChatGenerationRequest(
        system_prompt="Answer the question using only the provided context. If the answer is unavailable, say so briefly.",
        user_prompt=f"Context:\n{context}\n\nQuestion:\n{question}",
        max_output_tokens=260,
        temperature=0.1,
    )
    client = get_openai_client()
    response = client.responses.create(
        model=get_chat_model("qa", default_model="gpt-4.1-mini"),
        input=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt},
        ],
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
    )
    return AnswerResult(
        provider="OpenAI",
        model=response.model,
        answer=normalize_text(response.output_text),
        context_used=bool(context.strip()),
    )
