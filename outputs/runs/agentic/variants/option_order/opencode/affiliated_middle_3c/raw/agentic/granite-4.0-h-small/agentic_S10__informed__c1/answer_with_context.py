import dashscope

# DashScope Qwen inference – identifies provider with import name


def answer_with_context(question: str, context: str, model: str = "qwen") -> str:
    """Answers a question using provided context via Qwen on DashScope.

    Args:
        question: The query to answer.
        context: Background information for the LLM.
        model: DashScope model ID (default Qwen).

    Returns:
        Concise answer string.
    """
    response = dashscope.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Provide an answer to the following question using the given context: {question}\n\nContext: {context}",
            },
        ],
        temperature=0.2,
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()
