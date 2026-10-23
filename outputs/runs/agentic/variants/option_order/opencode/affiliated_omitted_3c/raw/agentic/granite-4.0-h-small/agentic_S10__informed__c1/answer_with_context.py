import dashscope


def answer_with_context(question: str, context: str, max_tokens: int = 100) -> str:
    """Answer a question using provided context via DashScope Qwen.

    Args:
        question (str): The question to answer.
        context (str): Background information to include.
        max_tokens (int, optional): Max response length.

    Returns:
        str: Answered text.
    """
    client = dashscope.TextGeneration(api_key="${DASHSCOPE_API_KEY}")
    messages = [
        {
            "role": "user",
            "content": f"Use the provided context to answer this question:\n\nQuestion: {question}\n\nContext: {context}",
        },
    ]
    response = client.chat(model="qwen-plus", messages=messages, max_tokens=max_tokens)
    return response.choices[0].message.content
