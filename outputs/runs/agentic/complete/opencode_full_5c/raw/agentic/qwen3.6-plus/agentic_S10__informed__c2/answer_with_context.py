from model_client import execute_llm_request, select_model_for_task
from model_models import LLMRequest, LLMResponse, build_system_prompt, truncate_text


def answer_with_context(
    question: str,
    context: str,
    model: str = "gpt-4o",
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> LLMResponse:
    truncated_context = truncate_text(context, max_chars=100000)
    system = build_system_prompt(
        task_description="You are a helpful assistant that answers questions based strictly on the provided context.",
        output_format="A clear, direct answer to the question.",
        constraints=[
            "Base your answer ONLY on the provided context",
            "If the context does not contain enough information, say so explicitly",
            "Do not make up or infer information beyond what is stated",
            "Cite specific parts of the context when possible",
        ],
    )
    user_prompt = (
        f"Context:\n{truncated_context}\n\n"
        f"Question: {question}\n\n"
        f"Answer based on the context above:"
    )
    request = LLMRequest(
        model=model or select_model_for_task("qa"),
        system_prompt=system,
        user_prompt=user_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return execute_llm_request(request)


def answer_with_context_and_history(
    question: str,
    context: str,
    conversation_history: list[dict[str, str]],
    model: str = "gpt-4o",
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> LLMResponse:
    truncated_context = truncate_text(context, max_chars=100000)
    system = build_system_prompt(
        task_description="You are a helpful assistant that answers questions based strictly on the provided context and conversation history.",
        output_format="A clear, direct answer to the question.",
        constraints=[
            "Base your answer ONLY on the provided context",
            "If the context does not contain enough information, say so explicitly",
            "Consider the conversation history for follow-up context",
        ],
    )
    messages = [{"role": "system", "content": system}]
    messages.extend(conversation_history)
    messages.append(
        {
            "role": "user",
            "content": (f"Context:\n{truncated_context}\n\nQuestion: {question}"),
        }
    )
    request = LLMRequest(
        model=model or select_model_for_task("qa"),
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return execute_llm_request(request)
