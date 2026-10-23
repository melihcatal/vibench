from model_client import get_client

def answer(question: str, context: str) -> str:
    """
    Answers a question based on the provided context using an OpenAI model.
    """
    client = get_client()
    prompt = f"""
    Based on the context below, please answer the question.
    If the answer cannot be found in the context, respond with "I don't know".

    Context:
    {context}

    Question:
    {question}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    
    answer_text = response.choices[0].message.content
    return answer_text.strip() if answer_text else ""
