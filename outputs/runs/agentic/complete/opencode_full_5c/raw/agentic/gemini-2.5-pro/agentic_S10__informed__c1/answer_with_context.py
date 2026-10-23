from model_client import get_openai_client


def answer_with_context(context: str, question: str) -> str:
    """
    Calls a hosted LLM to answer a question using provided context.
    """
    client = get_openai_client()

    prompt = f"""
    Based on the context provided below, please answer the user's question.
    If the answer cannot be found in the context, say "I cannot answer the question based on the provided context."

    Context:
    ---
    {context}
    ---

    Question: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful Q&A assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    if response.choices:
        return response.choices[0].message.content.strip()
    return ""
