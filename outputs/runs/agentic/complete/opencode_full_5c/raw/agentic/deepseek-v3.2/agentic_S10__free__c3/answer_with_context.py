from typing import Optional
from openai import OpenAI
from model_client import get_llm_client
from model_models import ContextAnswerRequest, ContextAnswerResponse


def answer_with_context(
    question: str, context: str, model: Optional[str] = None
) -> ContextAnswerResponse:
    """
    Answer a question using provided context with a hosted LLM.

    Args:
        question: The question to answer
        context: The context to use for answering
        model: Optional specific model to use

    Returns:
        ContextAnswerResponse containing the answer
    """
    client = get_llm_client()

    model_to_use = model or "gpt-4o"

    system_prompt = """You are a helpful assistant that answers questions based ONLY on the provided context.
    If the answer cannot be found in the context, say "I cannot answer based on the provided context."
    Do not use any external knowledge."""

    user_prompt = f"""Context: {context}

Question: {question}

Answer the question based ONLY on the context above."""

    try:
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.2,
        )

        answer = response.choices[0].message.content.strip()

        return ContextAnswerResponse(
            question=question,
            context=context,
            answer=answer,
            model_used=model_to_use,
            provider="openai",
        )

    except Exception as e:
        raise Exception(f"Failed to answer with context: {str(e)}")
