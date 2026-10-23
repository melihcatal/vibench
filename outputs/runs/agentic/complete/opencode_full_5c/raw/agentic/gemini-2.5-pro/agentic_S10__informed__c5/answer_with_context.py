from model_client import get_gemini_client


def answer_question_with_context_gemini(context: str, question: str) -> str:
    """
    Answers a question based on the provided context using the Gemini API.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Context:
    ---
    {context}
    ---
    
    Question: {question}
    
    Based on the context provided, please answer the question.
    """
    response = model.generate_content(prompt)
    return response.text
