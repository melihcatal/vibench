from model_client import get_google_client


def answer_with_context(context: str, question: str) -> str:
    model = get_google_client()
    prompt = f"""Using only the provided context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
    response = model.generate_content(prompt)
    return response.text.strip()
