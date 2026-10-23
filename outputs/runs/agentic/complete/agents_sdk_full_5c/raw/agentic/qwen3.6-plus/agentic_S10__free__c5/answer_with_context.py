"""
answer_with_context.py - Calls a hosted OpenAI LLM to answer a question using provided context.

Uses the OpenAI Chat Completions API with gpt-4o for contextual QA.
"""

from model_client import get_openai_client, select_model, build_chat_messages
from model_models import LLMResponse, build_context_qa_request


def answer_with_context(
    context: str,
    question: str,
    model_family: str = "gpt-4o",
    temperature: float = 0.3,
    max_tokens: int = 512,
) -> LLMResponse:
    """
    Answer a question using the provided context via OpenAI's hosted LLM.

    Args:
        context: The reference context text to ground the answer in.
        question: The question to answer.
        model_family: OpenAI model family (e.g. "gpt-4o", "gpt-4o-mini").
        temperature: Sampling temperature.
        max_tokens: Maximum tokens for the generated answer.

    Returns:
        LLMResponse containing the answer text and metadata.
    """
    request = build_context_qa_request(context, question, model_family)
    request.temperature = temperature
    request.max_tokens = max_tokens

    client = get_openai_client()
    model_id = select_model(request.model_family)

    messages = build_chat_messages(
        system_prompt=(
            "You are a helpful assistant powered by OpenAI. "
            "Answer questions based ONLY on the provided context. "
            "If the answer cannot be found in the context, respond with: "
            "\"The provided context does not contain enough information to answer this question.\""
        ),
        user_content=request.user_content,
        format_instructions=None,
    )

    params = request.to_openai_params(model=model_id, messages=messages)

    completion = client.chat.completions.create(**params)

    content = ""
    if completion.choices and completion.choices[0].message:
        content = completion.choices[0].message.content or ""

    usage = completion.usage
    return LLMResponse(
        text=content,
        model_used=model_id,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        finish_reason=completion.choices[0].finish_reason if completion.choices else "",
        raw_response=completion,
    )


def answer_multiple_questions(
    context: str,
    questions: list[str],
    model_family: str = "gpt-4o",
    temperature: float = 0.3,
) -> list[LLMResponse]:
    """
    Answer multiple questions against the same context.

    Args:
        context: The reference context.
        questions: List of questions to answer.
        model_family: OpenAI model family.
        temperature: Sampling temperature.

    Returns:
        List of LLMResponse objects, one per question.
    """
    results = []
    for q in questions:
        response = answer_with_context(context, q, model_family, temperature)
        results.append(response)
    return results


if __name__ == "__main__":
    ctx = (
        "The OpenAI GPT-4o model was released in May 2024. It is a multimodal model "
        "capable of processing text, images, and audio inputs. GPT-4o improved on its "
        "predecessor GPT-4 Turbo with faster response times and better performance on "
        "non-English language tasks. The model is available through the OpenAI API "
        "and powers the ChatGPT assistant. OpenAI also released a smaller variant "
        "called gpt-4o-mini which is more cost-effective for simpler tasks."
    )
    resp = answer_with_context(ctx, "When was GPT-4o released?", model_family="gpt-4o")
    print(f"Model: {resp.model_used}")
    print(f"Answer: {resp.text}")
    print(f"Tokens used: {resp.total_tokens}")
